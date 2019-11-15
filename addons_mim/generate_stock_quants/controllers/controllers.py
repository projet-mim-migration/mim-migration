# -*- coding: utf-8 -*-
from odoo import http

# class GenerateStockQuants(http.Controller):
#     @http.route('/generate_stock_quants/generate_stock_quants/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/generate_stock_quants/generate_stock_quants/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('generate_stock_quants.listing', {
#             'root': '/generate_stock_quants/generate_stock_quants',
#             'objects': http.request.env['generate_stock_quants.generate_stock_quants'].search([]),
#         })

#     @http.route('/generate_stock_quants/generate_stock_quants/objects/<model("generate_stock_quants.generate_stock_quants"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('generate_stock_quants.object', {
#             'object': obj
#         })