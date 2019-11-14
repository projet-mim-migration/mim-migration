# -*- coding: utf-8 -*-
from odoo import http

# class StockState(http.Controller):
#     @http.route('/stock_state/stock_state/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_state/stock_state/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_state.listing', {
#             'root': '/stock_state/stock_state',
#             'objects': http.request.env['stock_state.stock_state'].search([]),
#         })

#     @http.route('/stock_state/stock_state/objects/<model("stock_state.stock_state"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_state.object', {
#             'object': obj
#         })