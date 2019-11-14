# -*- coding: utf-8 -*-
from odoo import http

# class StockMrp(http.Controller):
#     @http.route('/stock_mrp/stock_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_mrp/stock_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_mrp.listing', {
#             'root': '/stock_mrp/stock_mrp',
#             'objects': http.request.env['stock_mrp.stock_mrp'].search([]),
#         })

#     @http.route('/stock_mrp/stock_mrp/objects/<model("stock_mrp.stock_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_mrp.object', {
#             'object': obj
#         })