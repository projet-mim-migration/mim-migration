# -*- coding: utf-8 -*-
from odoo import http

# class StockMimLivraison(http.Controller):
#     @http.route('/stock_mim_livraison/stock_mim_livraison/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_mim_livraison/stock_mim_livraison/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_mim_livraison.listing', {
#             'root': '/stock_mim_livraison/stock_mim_livraison',
#             'objects': http.request.env['stock_mim_livraison.stock_mim_livraison'].search([]),
#         })

#     @http.route('/stock_mim_livraison/stock_mim_livraison/objects/<model("stock_mim_livraison.stock_mim_livraison"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_mim_livraison.object', {
#             'object': obj
#         })