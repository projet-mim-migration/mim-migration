# -*- coding: utf-8 -*-

from odoo import fields, models


class MrpSubComponent(models.Model):
    _name = 'mrp.sub.component'
    
    name = fields.Char(
        'Désignation'
    )
    python_product_qty = fields.Text(
        'Quantité unitaire(QU)',
        required=True,
        default='result=0.0'
    )
    python_product_qty_total = fields.Text(
        'Quantité total (QT)',
        required=True,
        default='result=QU*Q'
    )
    python_len_unit = fields.Text(
        'Longueur unitaire (LU)',
        required=True,
        default='result=0.0'
    )
    python_len_total = fields.Text(
        'Longueur total (LT)',
        required=True,
        default='result=LU*QT'
    )
    component_id = fields.Many2one(
        'mrp.component',
        'Sous-composants', 
        ondelete='cascade'
    )