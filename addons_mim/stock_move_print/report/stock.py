
from odoo import models, fields, api

class move_parser(models.AbstractModel):

    def __init__(self, name):
        super(move_parser, self).__init__(name)
        self.localcontext.update({
                                  '_get_state_value': self._get_state_value,
                                  })
        #return self.env.ref('stock_move_reports').report_action(self)
    
    def _get_state_value(self, model, field, value):
 
        selection = self.env[model]._columns.get(field).selection
        val = ''
        for v in selection:
            if v[0] == value:
                val = v[1]
                break

        return val
        #return self.env.ref('stock_move_reports').report_action(val)


        
#('report.stock.move', 'stock.move', 'stock_move_print/report/stock_move.rml', parser=move_parser)

    #@api.multi
   # def print_quotation(self):
       # self.write({'state': "sent"})
       # return self.env.ref('stock_move_report').report_action(self)