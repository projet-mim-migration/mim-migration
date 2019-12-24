# -*- coding: utf-8 -*-
from odoo import models, fields

class Contre_mesure (models.Model):
    _name = 'contremesure'


    def _get_stock_move_id(self):
        if self.env.context is None: self.env.context = {}
        return self.env.context.get('stock_move_id', False)
    
    largeur = fields.Float('Largeur')
    hauteur = fields.Float('Hauteur')
    stock_move_id = fields.Integer('Id current stock move line',default=_get_stock_move_id)
    

    def update_contre_mesure(self):
        stock_move_id = self.stock_move_id
        self.env['stock.move'].search([('id','=',stock_move_id)]).write({'largeur':self.largeur,'hauteur': self.hauteur})
        self.env['stock.move'].browse(stock_move_id).contre_mesure1()
        