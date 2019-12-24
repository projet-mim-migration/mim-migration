# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ClaimReport(models.AbstractModel):
    _name = 'report.crm_claim_inherit.report_claim'

    @api.model
    def _get_report_values(self, docids, data=None):
        return{
            'doc_ids': docids,
            'doc_model': 'crm.claim',
            'docs': self.env['crm.claim'].browse(docids),
            'get_selection_value': self._get_selection_value,
        }

    def _get_selection_value(self, model, field, value):

        selection = self.env[model]._fields.get(field).selection
        val = ''
        res = ''
        for v in selection:
            if v[0] == value:
                val = v[1]
                break
        if val == 'Highest':
            res = 'La plus haute' 
        if val == 'High':
            res = 'Haute'
        if val == 'Normal':
            res = 'Normale'
        if val == 'Low':
            res = 'Basse'
        if val == 'Lowest':
            res = 'La plus basse'
            
        return res
