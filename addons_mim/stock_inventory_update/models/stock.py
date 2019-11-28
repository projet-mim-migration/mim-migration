# -*- coding: utf-8 -*-

from odoo import models, api


class stock_inventory_line(models.Model):
    _inherit = 'stock.inventory.line'

    @api.onchange('product_id', 'location_id')
    def onchange_createline(self):

        quant_obj = self.env['stock.quant']
        uom_obj = self.enc['uom.uom']
        res = {'value': {}}

        if self.product_id:
            product = self.env['product.product'].search(['id', '=', self.product_id])
            uom = self.env['uom.uom'].search(['id', '=', self.uom_id])

            res['value']['product_uom_id'] = product.uom_id.id
            res['domain'] = {'product_uom_id': [('category_id', '=', product.uom_id.category_id.id)]}
            uom_id = product.uom_id.id

        if self.product_id and self.location_id:
            product = self.env['product.product'].search(['id', '=', self.product_id])
            uom_id = product.uom_id.id

            if not self.company_id:
                company_id = self.env['res.users'].search(['id', '=', self.env.user.id])

            dom = [('company_id', '=', company_id), ('location_id', '=', self.location_id), ('lot_id', '=', self.prod_lot_id),
                   ('product_id', '=', self.product_id), ('owner_id', '=', self.partner_id), ('package_id', '=', self.package_id)]

            quants = quant_obj.search(dom)
            th_qty = sum([x.qty for x in quant_obj.search(quants)])

            if self.product_id and self.product_id.uom_id.id != self.uom_id:
                th_qty = uom_obj._compute_quantity(product.uom_id.id, th_qty, self.uom_id)

            res['valuer']['theoretical_qty'] = th_qty
            res['value']['product_qty'] = th_qty
