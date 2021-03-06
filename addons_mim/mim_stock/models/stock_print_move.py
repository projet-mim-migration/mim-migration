# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_move(models.Model):
    _inherit = "stock.move"
     
    def print_move(self):
        move_obj = self
        self.env.cr.execute("""SELECT id,date 
                               FROM stock_move 
                               WHERE date >= '%s' 
                               AND date <= '%s' 
                               ORDER BY date 
                               ASC""" % ('2016-01-01 00:00:00', '2016-12-31 23:59:59'))
        res = self.env.cr.fetchall()
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
