# -*- coding: utf-8 -*-
from odoo import http

# class StockBonLivraisonDatePrevue(http.Controller):
#     @http.route('/stock_bon_livraison_date_prevue/stock_bon_livraison_date_prevue/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_bon_livraison_date_prevue/stock_bon_livraison_date_prevue/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_bon_livraison_date_prevue.listing', {
#             'root': '/stock_bon_livraison_date_prevue/stock_bon_livraison_date_prevue',
#             'objects': http.request.env['stock_bon_livraison_date_prevue.stock_bon_livraison_date_prevue'].search([]),
#         })

#     @http.route('/stock_bon_livraison_date_prevue/stock_bon_livraison_date_prevue/objects/<model("stock_bon_livraison_date_prevue.stock_bon_livraison_date_prevue"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_bon_livraison_date_prevue.object', {
#             'object': obj
#         })