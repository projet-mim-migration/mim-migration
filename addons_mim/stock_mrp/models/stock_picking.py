# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

from datetime import datetime

class StockPicking(models.Model):
    _inherit = "stock.picking"

    
    @api.depends('date')
    def _get_late_production(self):
        res = {}
        fmt_datetime = DEFAULT_SERVER_DATETIME_FORMAT
        fmt_date = DEFAULT_SERVER_DATE_FORMAT
        
        for pick in self:
            if not pick.date:
                pick.late_production = False
                continue
            if pick.is_old_picking_assigned:
                pick.late_production = False
                continue
    
            date_delivery = str(pick.date)
            date_reference = str(datetime.now().strftime(fmt_datetime))
            if pick.production_date:
                date_reference = str(pick.production_date)
            
            d1 = datetime.strptime(str(datetime.strptime(date_reference, fmt_datetime).date()), fmt_date) 
            d2 = datetime.strptime(str(datetime.strptime(date_delivery, fmt_datetime).date()), fmt_date)  
            diff_date = d1 - d2
            days = diff_date.days
            pick.late_production = days


    @api.depends('date')
    def _get_late_delivery(self):
        res = {}
        fmt_datetime = DEFAULT_SERVER_DATETIME_FORMAT
        fmt_date = DEFAULT_SERVER_DATE_FORMAT
        
        for pick in self:
            if not pick.date:
                pick.late_delivery = False
                continue
            
            if pick.is_old_picking_done:
                pick.late_delivery = False
                continue
    
            date_delivery = str(pick.date)
            date_reference = str(datetime.now().strftime(fmt_datetime))
            if pick.delivery_date:
                date_reference = str(pick.delivery_date)
            
            d1 = datetime.strptime(str(datetime.strptime(date_reference, fmt_datetime).date()), fmt_date) 
            d2 = datetime.strptime(str(datetime.strptime(date_delivery, fmt_datetime).date()), fmt_date)  
            diff_date = d1 - d2
            days = diff_date.days
            pick.late_delivery = days

    
    @api.depends('move_lines')
    def _get_mo_created(self):        
        for pick in self:
            pick.mo_created_copy = pick.mo_created = False

            if any(move.id_mo for move in pick.move_lines):
                pick.mo_created_copy = pick.mo_created = True
            
    
    
    mo_created = fields.Boolean(
        string=u'Ordre de fabrication créé', 
        store=False,
        compute=_get_mo_created
    )
    late_production = fields.Float(
        string='Retard de production (jours)',
        compute=_get_late_production
    )
    production_date = fields.Datetime(
        'Date de fin production', 
        readonly=True
    )
    late_delivery = fields.Float(
        string='Retard de livraison (jours)', 
        compute=_get_late_delivery
    )
    delivery_date = fields.Datetime(
        'Date de fin livraison', 
        readonly=True
    )
    is_old_picking_assigned = fields.Boolean(
        u'Ancien BL disponible',
        default=False
    )
    is_old_picking_done = fields.Boolean(
        u'Ancien BL terminé',
        default=False
    )
    mo_created_copy = fields.Boolean(
        string=u'Ordre de fabrication créé ?'
    )
    

    @api.cr_uid_ids_context
    def split_picking(self, picking):
        ctx = {
            'active_model': self._name,
            'active_ids': picking['active_ids'],
            'active_id': picking['active_id'],
            'do_only_split': True,
        }

        self = self.with_context(ctx)
        
        created_id = self.env['stock.split_details'].create({'picking_id': picking['active_id']})
        
        return self.env['stock.split_details'].browse(created_id).wizard_view()
    
    @api.multi
    def confirm_config_mo(self):
        self.ensure_one()
        
        ctx = dict()
        ctx.update({
            'default_picking_id': self.id,
            'default_date_planned': self.date,
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
    
    @api.multi
    def view_all_mo(self):
        self.ensure_one()

        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        result = mod_obj.get_object_reference('mrp', 'mrp_production_action')
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]

        mo_ids = [p.id_mo for p in self.move_lines if p.id_mo]
        if len(mo_ids) < 1:
            return {}       
        else: 
            if len(mo_ids) > 1:
                result['domain'] = "[('id','in',["+','.join(map(str, mo_ids))+"])]"
            else:
                res = mod_obj.get_object_reference('mrp', 'mrp_production_form_view')
                result['views'] = [(res and res[1] or False, 'form')]
                result['res_id'] = mo_ids and mo_ids[0] or False
        
        return result
