# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class product_category(osv.osv):
    _inherit = "product.category"
    
    _columns = {
                'confirmed_wkf_ok' : fields.integer(string="Passe dans l'etat confirmé", help="Si sa valeur vaut 1 l'objet passera dans l'etat 'confirmé' du workflow (Purchase Order Basic Workflow), si 0 il sautera cet etat."),
                }
    _defaults = {
        'confirmed_wkf_ok' : 1,
    }
product_category()