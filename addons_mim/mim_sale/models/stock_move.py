# -*- coding: utf-8 -*-
from odoo import models, fields, api

class stock_move (models.Model):
	_inherit = 'stock.move'
	
	largeur = fields.Float('Largeur')
	hauteur = fields.Float('Hauteur')
	
	def edit_contre_mesure(self):
		ctx = dict()
		ctx.update({
			'default_stock_move_id': self.id
		})
		return {
			'name': 'Saisie Contre mesure',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'contremesure',
			'nodestroy': True,
			'target': 'new',
			'context': ctx,
		}