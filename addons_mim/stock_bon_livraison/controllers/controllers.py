# -*- coding: utf-8 -*-
from odoo import http

# class StockBonLivraison(http.Controller):
#     @http.route('/stock_bon_livraison/stock_bon_livraison/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_bon_livraison/stock_bon_livraison/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_bon_livraison.listing', {
#             'root': '/stock_bon_livraison/stock_bon_livraison',
#             'objects': http.request.env['stock_bon_livraison.stock_bon_livraison'].search([]),
#         })

#     @http.route('/stock_bon_livraison/stock_bon_livraison/objects/<model("stock_bon_livraison.stock_bon_livraison"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_bon_livraison.object', {
#             'object': obj
#         })