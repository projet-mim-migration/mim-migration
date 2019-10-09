# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class stock_picking(osv.osv):
    
    _inherit = 'stock.picking'
    _order = "create_date desc"
    
class mrp_production(osv.osv):
    
    _inherit = 'mrp.production'
    _order = "create_date desc"