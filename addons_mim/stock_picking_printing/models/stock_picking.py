# -*- coding: utf-8 -*-

from odoo import models, api, fields


class stock_picking_parser(models.Model):

    @api.model
    def init(self):
        super(stock_picking_parser, self).init()
        self.update({
            'get_description': self.get_description,
        })

    @api.model
    def get_description(self):
        id=self.ids[0]
        sql="""select stock_move.name,stock_move.product_qty 
        from stock_move inner join stock_picking 
        on stock_move.picking_id=stock_picking.id
        where stock_picking.id={0} order by stock_move.name asc""".format(id)
        self._cr.execute(sql)
        res = self._cr.fetchall()
        tab = []
        for x in range(len(res)):
            product_qty = int(res[x][1])
            for y in range(product_qty):
                name = u" "+res[x][0]+" "
                tab.append(name)
        return tab
#report_sxw.report_sxw('report.stock.picking', 'stock.picking', 'stock_picking_printing/report/rapport_stock.rml', parser=stock_picking_parser)