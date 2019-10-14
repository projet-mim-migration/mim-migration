# -*- coding: utf-8 -*-
from odoo import http

# class StockMim(http.Controller):
#     @http.route('/stock_mim/stock_mim/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_mim/stock_mim/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_mim.listing', {
#             'root': '/stock_mim/stock_mim',
#             'objects': http.request.env['stock_mim.stock_mim'].search([]),
#         })

#     @http.route('/stock_mim/stock_mim/objects/<model("stock_mim.stock_mim"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_mim.object', {
#             'object': obj
#         })