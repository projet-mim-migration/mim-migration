# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api


class stock_picking(models.Model):
    _inherit = "stock.picking"
    
    min_date = fields.Datetime('Date de contre-mesure', help="Date de contre-mesure", select=True, states={'done':[('readonly', True)], 'cancel':[('readonly',True)]}, default= lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    date = fields.Datetime('Date de livraison', help="Date de livraison", select=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))


class stock_picking_type(models.Model):
    _inherit = "stock.move"

    min_date = fields.Datetime('Date de contre-mesure', help="Date de contre-mesure", select=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    date = fields.Datetime('Date de livraison', help="Date de livraison", select=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))



                
                 
                 

