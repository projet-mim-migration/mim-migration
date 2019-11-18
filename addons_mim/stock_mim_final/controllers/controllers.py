# -*- coding: utf-8 -*-
from odoo import http

# class StockMimFinal(http.Controller):
#     @http.route('/stock_mim_final/stock_mim_final/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_mim_final/stock_mim_final/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_mim_final.listing', {
#             'root': '/stock_mim_final/stock_mim_final',
#             'objects': http.request.env['stock_mim_final.stock_mim_final'].search([]),
#         })

#     @http.route('/stock_mim_final/stock_mim_final/objects/<model("stock_mim_final.stock_mim_final"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_mim_final.object', {
#             'object': obj
#         })