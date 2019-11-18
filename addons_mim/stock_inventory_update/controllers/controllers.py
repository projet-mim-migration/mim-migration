# -*- coding: utf-8 -*-
from odoo import http

# class StockInventoryUpdate(http.Controller):
#     @http.route('/stock_inventory_update/stock_inventory_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_inventory_update/stock_inventory_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_inventory_update.listing', {
#             'root': '/stock_inventory_update/stock_inventory_update',
#             'objects': http.request.env['stock_inventory_update.stock_inventory_update'].search([]),
#         })

#     @http.route('/stock_inventory_update/stock_inventory_update/objects/<model("stock_inventory_update.stock_inventory_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_inventory_update.object', {
#             'object': obj
#         })