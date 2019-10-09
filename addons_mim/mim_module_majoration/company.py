# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class res_company(osv.osv):
    
    _inherit = "res.company"
    
    _columns = {
                'maj_globale': fields.float('Majoration globale'),
                'maj_note': fields.text('Note sur la majoration'),
                }
    _defaults = {
                 'maj_globale': 0.0,
             }