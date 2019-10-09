# -*- coding: utf-8 -*-
from openerp.osv import osv

class stock_picking(osv.osv):
    _name = 'stock.picking'
    #Héritage de l'objet stock.picking.out pour qu'il hérite 
    #de l'objet ir.needaction_mixin (bulles de notification de messages)
    _inherit = ['stock.picking','ir.needaction_mixin']
    
stock_picking()