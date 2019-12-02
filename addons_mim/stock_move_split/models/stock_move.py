# -*- coding: utf-8 -*-

from odoo import models, api


class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def modifier_inventaire(self):
        inventory_obj = self.env['stock.inventory']
        inventory_line_obj = self.env['stock.inventory.line']
        product_obj = self.pool.get('product.product')

        move_data = self
        inventory_id = inventory_obj.create({
            'name': 'INV ' + move_data.product_id.name,
            'filter': 'partial',
            'location_id': move_data.location_id.id,
            'state': 'draft',
        })

        prod_data = product_obj.browse(move_data.product_id.id)

        if prod_data.qty_available <= 0.0:
            qty_available = move_data.product_uom_qty
        else:
            qty_available = move_data.product_uom_qty + prod_data.qty_available

        line_data = {
            'inventory_id': inventory_id,
            'product_qty': qty_available,
            'location_id': move_data.location_id.id,
            'product_id': move_data.product_id.id,
            'product_uom_id': move_data.product_id.product_tmpl_id.uom_id.id,
        }

        inventory_line_obj.create(line_data)
        inventory_id.action_done()
        inventory_id.unlink()

        return True
