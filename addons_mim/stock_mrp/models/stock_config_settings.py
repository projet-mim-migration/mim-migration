# -*- coding: utf-8 -*-
from odoo import fields, models, api


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'
      
    def init_old_late(self):
        pick_obj = self.env['stock.picking']
        pick_ids = pick_obj.search([('state', 'in', ('assigned','done'))])
        for pick in pick_obj.browse(pick_ids):
            if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
                pick_obj.browse(pick.id).write({'is_old_picking_assigned': True})
            if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
                pick_obj.browse(pick.id).write({'is_old_picking_assigned': True})
                pick_obj.browse(pick.id).write({'is_old_picking_done': True})
        return True
