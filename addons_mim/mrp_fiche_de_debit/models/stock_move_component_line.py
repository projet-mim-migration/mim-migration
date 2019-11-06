# -*- coding: utf-8 -*-

from odoo import fields, models


#Cette classe servira à stocker les composants de la nomenclature
class MrpProductionProductComponentLine(models.Model):
    _name = 'stock.move.component.line'
    _description = 'Production component'
    
    ref = fields.Char(
        'Référence'
    )
    name = fields.Char(
        'Déscription'
    )
    product_qty = fields.Float(
        'Quantité unitaire'
    )
    product_qty_total = fields.Float(
        'Quantité total'
    )
    len_unit = fields.Float(
        'Longueur unitaire'
    )
    len_total = fields.Float(
        'Longueur total'
    )
    production_id = fields.Many2one(
        'mrp.production', 
        'Production Order', 
        select=True, 
        ondelete='cascade'
    )