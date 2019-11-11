# -*- coding: utf-8 -*-
from odoo import http

# class MimModuleCrmLead(http.Controller):
#     @http.route('/mim_module_crm_lead/mim_module_crm_lead/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mim_module_crm_lead/mim_module_crm_lead/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mim_module_crm_lead.listing', {
#             'root': '/mim_module_crm_lead/mim_module_crm_lead',
#             'objects': http.request.env['mim_module_crm_lead.mim_module_crm_lead'].search([]),
#         })

#     @http.route('/mim_module_crm_lead/mim_module_crm_lead/objects/<model("mim_module_crm_lead.mim_module_crm_lead"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mim_module_crm_lead.object', {
#             'object': obj
#         })