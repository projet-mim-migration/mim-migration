# -*- coding: utf-8 -*-
from odoo import http

# class StockPickingPrinting(http.Controller):
#     @http.route('/stock_picking_printing/stock_picking_printing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_printing/stock_picking_printing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_printing.listing', {
#             'root': '/stock_picking_printing/stock_picking_printing',
#             'objects': http.request.env['stock_picking_printing.stock_picking_printing'].search([]),
#         })

#     @http.route('/stock_picking_printing/stock_picking_printing/objects/<model("stock_picking_printing.stock_picking_printing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_printing.object', {
#             'object': obj
#         })