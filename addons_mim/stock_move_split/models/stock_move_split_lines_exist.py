# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class stock_move_split_lines_exist(models.TransientModel):
    _name = "stock.move.split.lines"
    _description = "Stock move Split lines"

    name = fields.char(string='Serial Number')
    quantity = fields.float(string='Quantity', digits=dp.get_precision('Product Unit Of Measure'))
    wizard_id = fields.many2one('stock.move.split', 'Parent Wizard')
    wizard_exist_id = fields.many2one('stock.move.split', 'Parent Wizard (for existing lines)')
    prodlot_id = fields.Many2one('stock.production.lot', string='Serial Number', domain="[('product_id','=',"
                                                                                        "parent.product_id)]")
    quantity = fields.Float(default=0.1)

    @api.onchange('prodlot_id')
    def onchange_lot_id(self):
        return self.env['stock.move'].onchange_lot_id()
