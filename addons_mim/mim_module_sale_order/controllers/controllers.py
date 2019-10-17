# -*- coding: utf-8 -*-
from odoo import http

# class MimModuleSaleOrder(http.Controller):
#     @http.route('/mim_module_sale_order/mim_module_sale_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mim_module_sale_order/mim_module_sale_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mim_module_sale_order.listing', {
#             'root': '/mim_module_sale_order/mim_module_sale_order',
#             'objects': http.request.env['mim_module_sale_order.mim_module_sale_order'].search([]),
#         })

#     @http.route('/mim_module_sale_order/mim_module_sale_order/objects/<model("mim_module_sale_order.mim_module_sale_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mim_module_sale_order.object', {
#             'object': obj
#         })