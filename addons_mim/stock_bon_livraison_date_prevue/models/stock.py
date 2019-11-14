# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api


class stock_move(models.Model):
    _inherit = "stock.move"

    date_prevue = fields.Datetime('Date prevue', help="Date prevue", select=True,
                               states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                               default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
