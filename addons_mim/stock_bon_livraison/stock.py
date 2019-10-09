# -*- coding: utf-8 -*-

import time
from openerp.osv import fields, osv

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
                'min_date': fields.datetime('Date de contre-mesure', help="Date de contre-mesure", 
                                        select=True, states={'done':[('readonly', True)], 'cancel':[('readonly',True)]}),
                }
    _defaults = {
                 'min_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
                 
                 }
stock_picking()
