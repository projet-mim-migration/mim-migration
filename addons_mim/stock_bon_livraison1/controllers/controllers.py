# -*- coding: utf-8 -*-
from odoo import http

# class StockBonLivraison1(http.Controller):
#     @http.route('/stock_bon_livraison1/stock_bon_livraison1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_bon_livraison1/stock_bon_livraison1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_bon_livraison1.listing', {
#             'root': '/stock_bon_livraison1/stock_bon_livraison1',
#             'objects': http.request.env['stock_bon_livraison1.stock_bon_livraison1'].search([]),
#         })

#     @http.route('/stock_bon_livraison1/stock_bon_livraison1/objects/<model("stock_bon_livraison1.stock_bon_livraison1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_bon_livraison1.object', {
#             'object': obj
#         })