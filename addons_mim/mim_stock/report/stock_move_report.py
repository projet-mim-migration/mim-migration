
from odoo import models, fields, api

class MoveParser(models.AbstractModel):
    _name = 'report.mim_stock.report_stock_move'

    @api.model
    def _get_report_values(self, docids, data=None):
        return{
            'doc_ids': docids,
            'doc_model': 'stock.move',
            'docs': self.env['stock.move'].browse(docids),
            'get_state_value': self._get_state_value,
        }
    

    def _get_state_value(self, model, field, value):
        selection = self.env[model]._fields.get(field).selection
        val = ''
        for v in selection:
            if v[0] == value:
                val = v[1]
                break

        return val