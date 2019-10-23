# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _name = 'stock.picking'
    #Héritage de l'objet stock.picking.out pour qu'il hérite 
    #de l'objet ir.needaction_mixin (bulles de notification de messages)
    #  ---- remove because useless since V9 'ir.needaction_mixin'
    _inherit = ['stock.picking']
    