# -*- coding: utf-8 -*-
from odoo import http

# class StockMovePrint(http.Controller):
#     @http.route('/stock_move_print/stock_move_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_move_print/stock_move_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_move_print.listing', {
#             'root': '/stock_move_print/stock_move_print',
#             'objects': http.request.env['stock_move_print.stock_move_print'].search([]),
#         })

#     @http.route('/stock_move_print/stock_move_print/objects/<model("stock_move_print.stock_move_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_move_print.object', {
#             'object': obj
#         })