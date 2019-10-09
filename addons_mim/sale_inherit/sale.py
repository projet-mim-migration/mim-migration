# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def _get_mesure(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for so_line in self.browse(cr, uid, ids, context=context):
            if so_line.largeur and so_line.hauteur:
                res[so_line.id] = str(int(so_line.largeur)) +"x"+ str(int(so_line.hauteur))
            else:
                res[so_line.id] = False
        return res    
    _columns = {
             'mesure': fields.function(_get_mesure, string='Dimension', type='char'),
     }
