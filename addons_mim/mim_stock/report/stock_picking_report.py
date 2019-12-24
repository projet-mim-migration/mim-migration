# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPickingPrinting(models.AbstractModel):
    _name = 'report.mim_stock.rapport_stock'

    @api.model
    def _get_report_values(self, docids, data=None):
        return{
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': self.env['stock.picking'].browse(docids),
            'get_description': self._get_description,
        }

    def _get_description(self, obj):
        self.env.cr.execute("""SELECT stock_move.name,stock_move.product_qty 
                           FROM stock_move 
                           INNER JOIN stock_picking 
                           ON stock_move.picking_id=stock_picking.id
                           WHERE stock_picking.id={0} 
                           ORDER BY stock_move.name 
                           ASC""".format(obj.id))
        res = self.env.cr.fetchall()
        tab = []
        for x in range(len(res)):
            product_qty = int(res[x][1])
            for y in range(product_qty):
                name = u" "+res[x][0]+" "
                tab.append(name)
        return tab