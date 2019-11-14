# -*- coding: utf-8 -*-
from odoo import http

# class StockMimNew(http.Controller):
#     @http.route('/stock_mim_new/stock_mim_new/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_mim_new/stock_mim_new/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_mim_new.listing', {
#             'root': '/stock_mim_new/stock_mim_new',
#             'objects': http.request.env['stock_mim_new.stock_mim_new'].search([]),
#         })

#     @http.route('/stock_mim_new/stock_mim_new/objects/<model("stock_mim_new.stock_mim_new"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_mim_new.object', {
#             'object': obj
#         })