# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    ####cette fonction permet de récupérer la référence du devis en cours de modification par ex SO003####
    @api.multi
    def action_mim_wizard(self):
        self.ensure_one()
        
        ctx = dict()
        order_ref = self.name[2:]
        ctx.update({
            'default_sujet' : 'Devis '+ self.name,
            'default_order_ref' : order_ref,
            'default_order_id' : self.id,
        })
        return {
            'name': 'Mim Wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mim.wizard',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }