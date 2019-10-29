# -*- coding: utf-8 -*-
from odoo import http

# class MimModuleCorrectionId(http.Controller):
#     @http.route('/mim_module_correction_id/mim_module_correction_id/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mim_module_correction_id/mim_module_correction_id/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mim_module_correction_id.listing', {
#             'root': '/mim_module_correction_id/mim_module_correction_id',
#             'objects': http.request.env['mim_module_correction_id.mim_module_correction_id'].search([]),
#         })

#     @http.route('/mim_module_correction_id/mim_module_correction_id/objects/<model("mim_module_correction_id.mim_module_correction_id"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mim_module_correction_id.object', {
#             'object': obj
#         })