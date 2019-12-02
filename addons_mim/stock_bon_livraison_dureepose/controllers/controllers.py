# -*- coding: utf-8 -*-
from odoo import http

# class StockBonLivraisonDureepose(http.Controller):
#     @http.route('/stock_bon_livraison_dureepose/stock_bon_livraison_dureepose/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_bon_livraison_dureepose/stock_bon_livraison_dureepose/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_bon_livraison_dureepose.listing', {
#             'root': '/stock_bon_livraison_dureepose/stock_bon_livraison_dureepose',
#             'objects': http.request.env['stock_bon_livraison_dureepose.stock_bon_livraison_dureepose'].search([]),
#         })

#     @http.route('/stock_bon_livraison_dureepose/stock_bon_livraison_dureepose/objects/<model("stock_bon_livraison_dureepose.stock_bon_livraison_dureepose"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_bon_livraison_dureepose.object', {
#             'object': obj
#         })