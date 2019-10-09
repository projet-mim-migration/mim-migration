from openerp.report import report_sxw

class stock_picking_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(stock_picking_parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
        'get_description':self.get_description,
        })
    def get_description(self):
        id=self.ids[0]
        sql="""select stock_move.name,stock_move.product_qty 
        from stock_move inner join stock_picking 
        on stock_move.picking_id=stock_picking.id
        where stock_picking.id={0} order by stock_move.name asc""".format(id)
        self.cr.execute(sql)
        res = self.cr.fetchall()
        tab = []
        for x in range(len(res)):
            product_qty = int(res[x][1])
            for y in range(product_qty):
                name = u" "+res[x][0]+" "
                tab.append(name)
        return tab
report_sxw.report_sxw('report.stock.picking', 'stock.picking', 'stock_picking_printing/report/rapport_stock.rml', parser=stock_picking_parser)