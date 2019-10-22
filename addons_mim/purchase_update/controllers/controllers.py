# -*- coding: utf-8 -*-
from odoo import http

# class PurchaseUpdate(http.Controller):
#     @http.route('/purchase_update/purchase_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_update/purchase_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_update.listing', {
#             'root': '/purchase_update/purchase_update',
#             'objects': http.request.env['purchase_update.purchase_update'].search([]),
#         })

#     @http.route('/purchase_update/purchase_update/objects/<model("purchase_update.purchase_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_update.object', {
#             'object': obj
#         })