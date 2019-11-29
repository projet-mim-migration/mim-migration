# -*- coding: utf-8 -*-

from odoo import models, api, exceptions


class stock_inventory_line(models.Model):
    _inherit = 'stock.inventory.line'

    @api.onchange('product_id', 'location_id')
    def onchange_createline(self):

        quant_obj = self.env['stock.quant']
        uom_obj = self.env['uom.uom']
        res = {'value': {}}

        if self.product_id:
            product = self.env['product.product'].search([('id', '=', self.product_id.id)])
            uom = self.env['uom.uom'].search([('id', '=', self.product_uom_id.id)])

            res['value']['product_uom_id'] = product.uom_id.id
            res['domain'] = {'product_uom_id': [('category_id', '=', product.uom_id.category_id.id)]}
            uom_id = product.uom_id.id

        # Calculate theoretical quantity by searching the quants as in quants_get
        if self.product_id and self.location_id:
            product = self.env['product.product'].search([('id', '=', self.product_id.id)])
            uom_id = product.uom_id.id

            if not self.company_id:
                company_id = self.env['res.users'].search([('id', '=', self.env.user.id)])

            dom = [('company_id', '=', self.company_id.id), ('location_id', '=', self.location_id.id), ('lot_id', '=', self.prod_lot_id.id),
                   ('product_id', '=', self.product_id.id), ('owner_id', '=', self.partner_id.id), ('package_id', '=', self.package_id.id)]

            quants = quant_obj.search(dom)
            th_qty = sum([x.quantity for x in quants])

            if self.product_id and self.product_id.uom_id != self.product_uom_id:
                th_qty = uom_obj._compute_quantity(product.uom_id.id, th_qty, self.product_uom_id)

            res['value']['theoretical_qty'] = th_qty
            res['value']['product_qty'] = th_qty
