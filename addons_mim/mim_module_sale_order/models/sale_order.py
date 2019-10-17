# -*- coding: utf-8 -*-
from odoo import models, fields, api


class mim_sale_order(models.Model):
    _inherit = 'sale.order'
    
    crm_lead_id = fields.Many2one('crm.lead', u'Opportunité', select=True, track_visibility='onchange')
