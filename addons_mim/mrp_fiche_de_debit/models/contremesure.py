# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ContreMesure(models.Model):
    _name = 'contremesure'


    def _get_stock_move_id():
        context = dict(self._context or {})
        return context.get('stock_move_id', False)

    largeur = fields.Float(
        string='Largeur',
    )
    hauteur = fields.Float(
        string='Hauteur',
    )
    stock_move_id = fields.Integer(
        string='Id current stock move line',
        default=_get_stock_move_id
    )
    
    @api.multi
    def update_contre_mesure(self):
        self.ensure_one()
        
        self.env['stock.move'].browse(self.stock_move_id).write({
            'largeur' : self.largeur,
            'hauteur': self.hauteur
        })
        