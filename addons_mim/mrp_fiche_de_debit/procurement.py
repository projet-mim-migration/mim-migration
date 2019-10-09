# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp import netsvc

class procurement_order(osv.osv):
    _inherit = 'procurement.order'
    
    """def make_mo(self, cr, uid, ids, context=None):
        procurement_obj = self.pool.get('procurement.order')
        for procurement in procurement_obj.browse(cr, uid, ids, context=context):
            procurement_obj.action_done(cr, uid, [procurement.id])
        return {}"""
        
procurement_order()