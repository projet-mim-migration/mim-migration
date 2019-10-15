# -*- coding: utf-8 -*-
from odoo import http

# class MimModuleMajoration(http.Controller):
#     @http.route('/mim_module_majoration/mim_module_majoration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mim_module_majoration/mim_module_majoration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mim_module_majoration.listing', {
#             'root': '/mim_module_majoration/mim_module_majoration',
#             'objects': http.request.env['mim_module_majoration.mim_module_majoration'].search([]),
#         })

#     @http.route('/mim_module_majoration/mim_module_majoration/objects/<model("mim_module_majoration.mim_module_majoration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mim_module_majoration.object', {
#             'object': obj
#         })