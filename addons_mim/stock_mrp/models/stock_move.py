# -*- coding: utf-8 -*-
from odoo import fields, models, api

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class StockMove(models.Model):
    _inherit = "stock.move"
    
    name = fields.Text(
        'Description', 
        required=True, 
        select=True
    )
    
    def write(self, vals):
        context = self.env.context or {}
        res = super(StockMove, self).write(vals)
        
        #mise a jour ordre de fabrication
        if vals.get('largeur') or vals.get('hauteur') or vals.get('is_printable'):
            mo_vals = {
                       'largeur':self.largeur,
                       'hauteur': self.hauteur,
                       'is_printable': self.is_printable,
                       }
            self.env['mrp.production'].browse(self.id_mo).write(mo_vals)
        
        #mise a jour date de production
        pick_obj = self.env['stock.picking']
        date_now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if vals.get('state'):
            for move in self:
                pick = pick_obj.browse(move.picking_id.id)
                if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
                    pick_obj.browse(pick.id).write({'production_date': date_now})
                if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
                    pick_obj.browse(pick.id).write({'delivery_date': date_now})
        return res
