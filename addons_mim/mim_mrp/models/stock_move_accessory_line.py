# -*- coding: utf-8 -*-

from odoo import fields, models


#Cette classe servira à stocker les accessoires de la nomenclature
class MrpProductionProductAccessoryLine(models.Model):
    _name = 'stock.move.accessory.line'
    _description = 'Production accessory'
    
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
    production_id = fields.Many2one(
        'mrp.production', 
        'Production Order', 
        select=True, 
        ondelete='cascade'
    )