# -*- coding: utf-8 -*-
from odoo import http

# class MimModule(http.Controller):
#     @http.route('/mim_module/mim_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mim_module/mim_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mim_module.listing', {
#             'root': '/mim_module/mim_module',
#             'objects': http.request.env['mim_module.mim_module'].search([]),
#         })

#     @http.route('/mim_module/mim_module/objects/<model("mim_module.mim_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mim_module.object', {
#             'object': obj
#         })