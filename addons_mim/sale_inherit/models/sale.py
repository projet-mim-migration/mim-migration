# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    mesure = fields.Char(
        string='Dimension',
        compute="_get_mesure"
    )

    largeur = fields.Float(
        string='Largeur',
    )
    hauteur = fields.Float(
        string='Hauteur',
    )


    @api.depends('largeur', 'hauteur')
    def _get_mesure(self):
        for so_line in self:
            if so_line.largeur and so_line.hauteur:
                so_line.mesure = str(int(so_line.largeur)) +"x"+ str(int(so_line.hauteur))
            else:
                so_line.mesure = False
