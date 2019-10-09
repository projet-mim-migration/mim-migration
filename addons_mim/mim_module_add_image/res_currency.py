# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields

class res_currency(osv.osv):
    _inherit = 'res.currency'
    _columns = {
                'currency_name':fields.char('Nom complet devise',size=20),
                }
res_currency()