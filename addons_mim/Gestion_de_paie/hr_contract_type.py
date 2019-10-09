# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields

class hr_contract_type (osv.osv):
    _inherit = 'hr.contract.type'
    _columns = {
                'val_prime': fields.float('Valeur de la prime'),
                }
hr_contract_type()