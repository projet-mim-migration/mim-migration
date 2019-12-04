# -*- coding: utf-8 -*-
from odoo import models, fields, api

class res_company(models.Model):
	
	_inherit = "res.company"
	
	maj_globale = fields.Float('Majoration globale',default=0.0)
	maj_note = fields.Text('Note sur la majoration')