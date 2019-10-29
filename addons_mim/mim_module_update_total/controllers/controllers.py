# -*- coding: utf-8 -*-
from odoo import http

# class MimModuleUpdateTotal(http.Controller):
#     @http.route('/mim_module_update_total/mim_module_update_total/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mim_module_update_total/mim_module_update_total/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mim_module_update_total.listing', {
#             'root': '/mim_module_update_total/mim_module_update_total',
#             'objects': http.request.env['mim_module_update_total.mim_module_update_total'].search([]),
#         })

#     @http.route('/mim_module_update_total/mim_module_update_total/objects/<model("mim_module_update_total.mim_module_update_total"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mim_module_update_total.object', {
#             'object': obj
#         })