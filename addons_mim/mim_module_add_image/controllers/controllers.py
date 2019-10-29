# -*- coding: utf-8 -*-
from odoo import http

# class MimModuleAddImage(http.Controller):
#     @http.route('/mim_module_add_image/mim_module_add_image/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mim_module_add_image/mim_module_add_image/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mim_module_add_image.listing', {
#             'root': '/mim_module_add_image/mim_module_add_image',
#             'objects': http.request.env['mim_module_add_image.mim_module_add_image'].search([]),
#         })

#     @http.route('/mim_module_add_image/mim_module_add_image/objects/<model("mim_module_add_image.mim_module_add_image"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mim_module_add_image.object', {
#             'object': obj
#         })