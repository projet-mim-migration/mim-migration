# -*- coding: utf-8 -*-

from odoo import models, fields, api

class stock_picking(models.Model):
    
    _inherit = 'stock.picking'
    _order = "create_date desc"
    
class mrp_production(models.Model):
    
    _inherit = 'mrp.production'
    _order = "create_date desc"