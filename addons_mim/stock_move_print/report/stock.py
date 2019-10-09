from openerp.report import report_sxw

class move_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(move_parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
                                  '_get_state_value': self._get_state_value,
                                  })
    
    def _get_state_value(self, model, field, value):
 
        selection = self.pool.get(model)._columns.get(field).selection
        val = ''
        for v in selection:
            if v[0] == value:
                val = v[1]
                break
        return val
        
report_sxw.report_sxw('report.stock.move', 'stock.move', 'stock_move_print/report/stock_move.rml', parser=move_parser)