# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"
    
    def _update_quantity(self):
        production_id = self.env.context.get('active_id', False)
        current_production = self.env['mrp.production'].browse(production_id)
        for raw_material in self.produce_line_ids:
            current_material = current_production.move_raw_ids.filtered(lambda x: x.product_id == raw_material.product_id)
            raw_material.qty_to_consume = current_material.product_uom_qty
            raw_material.qty_reserved = raw_material.qty_to_consume
            raw_material.qty_done = raw_material.qty_to_consume


    @api.onchange('product_qty')
    def _onchange_product_qty(self):
        super(MrpProductProduce, self)._onchange_product_qty()
        self._update_quantity()

    
    @api.multi
    def do_produce(self):
        production_id = self._context.get('active_id', False)
        # state_move = self.env['stock.move'].search([('id_mo', '=', self.production_id.id)]).state
        # print("\nproduction_id : ",production_id,"\n")
        self.env['stock.move'].search([('id_mo', '=', production_id)]).state = 'flowsheeting'
        
        self.env['mrp.production'].browse(production_id).state = 'progress'
        return super(MrpProductProduce, self).do_produce()
        