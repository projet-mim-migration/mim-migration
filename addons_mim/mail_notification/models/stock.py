# -*- coding: utf-8 -*-

from odoo import models, fields


class StockPicking(models.Model):
    _name = 'stock.picking'
    #Héritage de l'objet stock.picking.out pour qu'il hérite 
    #de l'objet ir.needaction_mixin (bulles de notification de messages)
    #  ---- 'ir.needaction_mixin' removed and replaced with 'mail.activity.mixin'
    _inherit = ['mail.activity.mixin', 'stock.picking']
    