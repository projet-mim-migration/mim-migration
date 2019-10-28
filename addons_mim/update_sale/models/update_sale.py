# -*- coding: utf-8 -*-

from odoo import fields, models


class sale_order_line(models.Model):

    _inherit = 'sale.order.line'

    price_unit = fields.Float(
        string='Unit Price',
        required=True,
        readonly=True,
    )
