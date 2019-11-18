# -*- coding: utf-8 -*-
from odoo import http

# class StockBonLivraisonFinal1(http.Controller):
#     @http.route('/stock_bon_livraison_final1/stock_bon_livraison_final1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_bon_livraison_final1/stock_bon_livraison_final1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_bon_livraison_final1.listing', {
#             'root': '/stock_bon_livraison_final1/stock_bon_livraison_final1',
#             'objects': http.request.env['stock_bon_livraison_final1.stock_bon_livraison_final1'].search([]),
#         })

#     @http.route('/stock_bon_livraison_final1/stock_bon_livraison_final1/objects/<model("stock_bon_livraison_final1.stock_bon_livraison_final1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_bon_livraison_final1.object', {
#             'object': obj
#         })