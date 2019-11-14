# -*- coding: utf-8 -*-
from odoo import http

# class StockMimButtom(http.Controller):
#     @http.route('/stock_mim_buttom/stock_mim_buttom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_mim_buttom/stock_mim_buttom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_mim_buttom.listing', {
#             'root': '/stock_mim_buttom/stock_mim_buttom',
#             'objects': http.request.env['stock_mim_buttom.stock_mim_buttom'].search([]),
#         })

#     @http.route('/stock_mim_buttom/stock_mim_buttom/objects/<model("stock_mim_buttom.stock_mim_buttom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_mim_buttom.object', {
#             'object': obj
#         })