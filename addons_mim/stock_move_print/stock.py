from openerp.osv import osv

class stock_move(osv.osv):
    _inherit = "stock.move"
     
    def print_move(self, cr, uid, ids, context=None):
        move_obj = self.browse(cr,uid,ids,context)[0]
        cr.execute("SELECT id,date FROM stock_move WHERE date >= '%s' AND date <= '%s' ORDER BY date asc" % ('2016-01-01 00:00:00', '2016-12-31 23:59:59'))
        res = cr.fetchall()
        move_ids = []
        for id in range(len(res)):
            move_ids.append(res[id][0])
        datas = {
                 'model': 'stock.move',
                 'ids': move_ids,
                 }
        return {
                'type': 'ir.actions.report.xml', 
                'report_name': 'stock.move', 
                'datas': datas, 
                'nodestroy': True
                }
