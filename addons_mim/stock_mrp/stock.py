# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import osv, fields
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp import SUPERUSER_ID

#MAX_OLD_ID = 14580

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    def _get_late(self, cr, uid, ids, name, args, context=None):
        res = {}
        fmt_datetime = DEFAULT_SERVER_DATETIME_FORMAT
        fmt_date = DEFAULT_SERVER_DATE_FORMAT
        for pick in self.browse(cr, uid, ids, context=context):
            if not pick.date: 
                res[pick.id] = False
                continue
            if pick.is_old_picking_assigned and name == 'late_production':
                res[pick.id] = False
                continue
            if pick.is_old_picking_done and name == 'late_delivery':
                res[pick.id] = False
                continue
    
            date_delivery = str(pick.date)
            date_reference = str(datetime.now().strftime(fmt_datetime))
            if name == 'late_production' and pick.production_date:
                date_reference = str(pick.production_date)
            if name == 'late_delivery' and pick.delivery_date:
                date_reference = str(pick.delivery_date)
            d1=datetime.strptime(str(datetime.strptime(date_reference, fmt_datetime).date()), fmt_date) 
            d2=datetime.strptime(str(datetime.strptime(date_delivery, fmt_datetime).date()), fmt_date)  
            diff_date = d1-d2
            days = diff_date.days
            res[pick.id] = days
        return res
    
    def _get_mo_created(self, cr, uid, ids, name, args, context=None):
        res = {}
        pick_oj = self.pool.get('stock.picking')
        for pick in self.browse(cr, uid, ids, context=context):
            res[pick.id] = False
            if any(move.id_mo for move in pick.move_lines):
                res[pick.id] = True
            pick_oj.write(cr, SUPERUSER_ID, [pick.id], {'mo_created_copy': res[pick.id]}, context=context)
        return res
    
    _columns = {
                'mo_created': fields.function(_get_mo_created, type='boolean', string=u'Ordre de fabrication créé', store=False),
                'late_production': fields.function(_get_late, type='float', string='Retard de production (jours)'),
                'production_date': fields.datetime('Date de fin production', readonly=True),
                'late_delivery': fields.function(_get_late, type='float', string='Retard de livraison (jours)'),
                'delivery_date': fields.datetime('Date de fin livraison', readonly=True),
                'is_old_picking_assigned': fields.boolean(u'Ancien BL disponible'),
                'is_old_picking_done': fields.boolean(u'Ancien BL terminé'),
                'mo_created_copy': fields.boolean(string=u'Ordre de fabrication créé ?'),
              }
    _defaults = {
                 'is_old_picking_assigned': False,
                 'is_old_picking_done': False
                 }
    

    @api.cr_uid_ids_context
    def split_picking(self, cr, uid, picking, context=None):
        ctx = {
            'active_model': self._name,
            'active_ids': picking,
            'active_id': len(picking) and picking[0] or False,
            'do_only_split': True,
        }
        created_id = self.pool['stock.split_details'].create(cr, uid, {'picking_id': len(picking) and picking[0] or False}, ctx)
        return self.pool['stock.split_details'].wizard_view(cr, uid, created_id, ctx)
    
    def confirm_config_mo(self, cr, uid, ids, context=None):
        ctx = dict()
        picking = self.browse(cr, uid, ids, context=context)[0]
        ctx.update({
            'default_picking_id': picking.id,
            'default_date_planned': picking.date,
        })
        return {
            'name': u'Veuillez entrer la date prévue',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.configuration',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }
    
    def view_all_mo(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(cr, uid, 'mrp', 'mrp_production_action')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        pick = self.browse(cr, uid, ids, context=context)[0]
        mo_ids = [p.id_mo for p in pick.move_lines if p.id_mo]
        if len(mo_ids)<1:
            return {}       
        else: 
            if len(mo_ids)>1:
                result['domain'] = "[('id','in',["+','.join(map(str, mo_ids))+"])]"
            else:
                res = mod_obj.get_object_reference(cr, uid, 'mrp', 'mrp_production_form_view')
                result['views'] = [(res and res[1] or False, 'form')]
                result['res_id'] = mo_ids and mo_ids[0] or False
        
        return result
        
class stock_move(osv.osv):
    _inherit = "stock.move"
    
    _columns = {
                'name': fields.text('Description', required=True, select=True),
                }
    
    def write(self, cr, uid, ids, vals, context=None):
        context = context or {}
        res = super(stock_move, self).write(cr, uid, ids, vals, context=context)
        
        #mise a jour ordre de fabrication
        if vals.get('largeur') or vals.get('hauteur') or vals.get('is_printable'):
            mo_vals = {
                       'largeur':self.browse(cr, uid, ids, context=context)[0].largeur,
                       'hauteur': self.browse(cr, uid, ids, context=context)[0].hauteur,
                       'is_printable': self.browse(cr, uid, ids, context=context)[0].is_printable,
                       }
            mrp_prod_id = self.browse(cr, uid, ids, context=context)[0].id_mo
            self.pool.get('mrp.production').write(cr, uid, [mrp_prod_id], mo_vals, context=context)
        
        #mise a jour date de production
        pick_obj = self.pool.get('stock.picking')
        date_now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if vals.get('state'):
            for move in self.browse(cr, uid, ids, context=context):
                pick = pick_obj.browse(cr, uid, move.picking_id.id, context=context)
                if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
                    pick_obj.write(cr, uid, [pick.id], {'production_date': date_now}, context=context)
                if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
                    pick_obj.write(cr, uid, [pick.id], {'delivery_date': date_now}, context=context)    
        return res
    

class stock_config_settings(osv.osv_memory):
    _inherit = 'stock.config.settings'
      
    def init_old_late(self, cr, uid, ids, context=None):
        pick_obj = self.pool.get('stock.picking')
        pick_ids = pick_obj.search(cr, uid, [('state', 'in', ('assigned','done'))], context=context)
        for pick in pick_obj.browse(cr, uid, pick_ids, context=context):
            if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
                pick_obj.write(cr, uid, [pick.id], {'is_old_picking_assigned': True}, context=context)
            if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
                pick_obj.write(cr, uid, [pick.id], {'is_old_picking_assigned': True}, context=context)
                pick_obj.write(cr, uid, [pick.id], {'is_old_picking_done': True}, context=context)
        return True
