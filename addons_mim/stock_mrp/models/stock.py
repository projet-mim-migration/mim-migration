# -*- coding: utf-8 -*-
import time
import _strptime
from datetime import datetime

from odoo  import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import SUPERUSER_ID


#MAX_OLD_ID = 14580

class stock_picking(models.Model):
    _inherit = "stock.picking"

    def _get_late(self):
        res = {}
        fmt_datetime = DEFAULT_SERVER_DATETIME_FORMAT
        fmt_date = DEFAULT_SERVER_DATE_FORMAT
        for pick in self.browse():
            if not pick.date:
                res[pick.id] = False
                continue
            if pick.is_old_picking_assigned and self == 'late_production':
                res[pick.id] = False
                continue
            if pick.is_old_picking_done and self == 'late_delivery':
                res[pick.id] = False
                continue

            date_delivery = str(pick.date)
            date_reference = str(datetime.now()._strptime(fmt_datetime))
            if self == 'late_production' and pick.production_date:
                date_reference = str(pick.production_date)
            if self == 'late_delivery' and pick.delivery_date:
                date_reference = str(pick.delivery_date)
            d1 = datetime._strptime(str(datetime._strptime(date_reference, fmt_datetime).date()), fmt_date)
            d2 = datetime._strptime(str(datetime.strptime(date_delivery, fmt_datetime).date()), fmt_date)
            diff_date = d1 - d2
            days = diff_date.days
            res[pick.id] = days
        return res

    def _get_mo_created(self):
        res = {}
        pick_oj = self.env['stock.picking']
        for pick in self:
            res[pick.id] = False
            if any(move.move_line_ids for move in pick.move_lines):
                res[pick.id] = True
            pick_oj.write({'mo_created_copy': res[pick.id]})
            #pick_oj.write(cr, SUPERUSER_ID, [pick.id], {'mo_created_copy': res[pick.id]}, context=context)
        return res


    mo_created = fields.Boolean(string='Ordre de fabrication créé', compute=_get_mo_created)
    late_production = fields.Float(string='Retard de production (jours)', compute=_get_late)
    production_date = fields.Datetime('Date de fin production', readonly=True)
    late_delivery = fields.Float(string='Retard de livraison (jours)', compute=_get_late)
    delivery_date = fields.Datetime('Date de fin livraison', readonly=True)
    is_old_picking_assigned = fields.Boolean('Ancien BL disponible', default=False)
    is_old_picking_done = fields.Boolean('Ancien BL terminé', default=False)
    mo_created_copy = fields.Boolean(string='Ordre de fabrication créé ?')

    @api.model
    @api.one
    def split_picking(self, picking):
        ctx = {
            'active_model': self._name,
            'active_ids': picking,
            'active_id': len(picking) and picking[0] or False,
            'do_only_split': True,
        }
        created_id = self.env['stock.split_details'].create({'picking_id': len(picking) and picking[0] or False}, ctx)
        return self.env['stock.split_details'].wizard_view(created_id, ctx)

    def confirm_config_mo(self):
        ctx = dict()
        picking = self.browse()[0]
        ctx.update({
            'default_picking_id': picking.id,
            'default_date_planned': picking.date,
        })
        return {
            'name': 'Veuillez entrer la date prévue',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.configuration',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }

    def view_all_mo(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        result = mod_obj.get_object_reference('mrp', 'mrp_production_action')
        id = result and result[1] or False
        result = act_obj.read([id])[0]
        pick = self.browse()[0]
        mo_ids = [p.id_mo for p in pick.move_lines if p.id_mo]
        if len(mo_ids) < 1:
            return {}
        else:
            if len(mo_ids) > 1:
                result['domain'] = "[('id','in',[" + ','.join(map(str, mo_ids)) + "])]"
            else:
                res = mod_obj.get_object_reference('mrp', 'mrp_production_form_view')
                result['views'] = [(res and res[1] or False, 'form')]
                result['res_id'] = mo_ids and mo_ids[0] or False
        return result


class stock_move(models.Model):
    _inherit = "stock.move"

    name = fields.Text('Description', required=True, select=True)

    def write(self, vals):
        context = self.env.context or {}
        res = super(stock_move, self).write(vals)

        # mise a jour ordre de fabrication
        if vals.get('largeur') or vals.get('hauteur') or vals.get('is_printable'):
            mo_vals = {
                'largeur': self.browse()[0].largeur,
                'hauteur': self.browse()[0].hauteur,
                'is_printable': self.browse()[0].is_printable,
            }
            mrp_prod_id = self.browse()[0].id_mo
            self.env['mrp.production'].write([mrp_prod_id], mo_vals)

        # mise a jour date de production
        pick_obj = self.pool.get('stock.picking')
        date_now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if vals.get('state'):
            for move in self.browse():
                pick = pick_obj.browse(move.picking_id.id)
                if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
                    pick_obj.write([pick.id], {'production_date': date_now})
                if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
                    pick_obj.write([pick.id], {'delivery_date': date_now})
        return res


#class stock_config_settings(models.TransientModel):
 #   _inherit = 'stock.config.settings'

#     def init_old_late(self):
#        pick_obj = self.env['stock.picking']
#        pick_ids = pick_obj.search(self.env.cr, self.env.uid, [('state', 'in', ('assigned', 'done'))], context=self.env.context)
#        for pick in pick_obj.browse(self.env.cr, self.env.uid, pick_ids, context=self.env.context):
 #           if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
  #              pick_obj.write(self.env.cr, self.env.uid, [pick.id], {'is_old_picking_assigned': True}, context=self.env.context)
  #          if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
   #             pick_obj.write(self.env.cr, self.env.uid, [pick.id], {'is_old_picking_assigned': True}, context=self.env.context)
   #             pick_obj.write(self.env.cr, self.env.uid, [pick.id], {'is_old_picking_done': True}, context=self.env.context)
   #     return True
