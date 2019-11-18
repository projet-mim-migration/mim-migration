# -*- coding: utf-8 -*-
from odoo import http

# class StockMoveSplit(http.Controller):
#     @http.route('/stock_move_split/stock_move_split/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_move_split/stock_move_split/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_move_split.listing', {
#             'root': '/stock_move_split/stock_move_split',
#             'objects': http.request.env['stock_move_split.stock_move_split'].search([]),
#         })

#     @http.route('/stock_move_split/stock_move_split/objects/<model("stock_move_split.stock_move_split"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_move_split.object', {
#             'object': obj
#         })