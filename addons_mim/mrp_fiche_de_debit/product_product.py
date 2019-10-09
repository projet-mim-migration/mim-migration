# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
                'ref': fields.char(string=u'Référence'),
                }
    #_sql_constraints = [('ref_unique', 'unique(ref)', u'Cette RÃ©fÃ©rence existe dÃ©jÃ !')]
    
product_product()