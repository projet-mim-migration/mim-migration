# -*- coding: utf-8 -*-
from openerp.osv import fields
from openerp.osv import osv


class mim_sale_order (osv.osv):
    _inherit = 'sale.order'
    
    _columns = {
        'crm_lead_id': fields.many2one('crm.lead', u'Opportunité', select=True, track_visibility='onchange'),
    }

mim_sale_order()
