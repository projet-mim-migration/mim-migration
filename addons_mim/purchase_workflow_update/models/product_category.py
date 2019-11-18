# -*- coding: utf-8 -*-
from odoo import fields, models



class ProductCategory(models.Model):
    _inherit = "product.category"
    
    
    confirmed_wkf_ok = fields.Integer(
        string="Passe dans l'etat confirmé", 
        help="Si sa valeur vaut 1 l'objet passera dans l'etat 'confirmé' du workflow (Purchase Order Basic Workflow), si 0 il sautera cet etat.",
        default=1
    )
    