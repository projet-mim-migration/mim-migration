# -*- coding: utf-8 -*-
from odoo import http

# class CrmLead(http.Controller):
#     @http.route('/crm_lead/crm_lead/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_lead/crm_lead/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_lead.listing', {
#             'root': '/crm_lead/crm_lead',
#             'objects': http.request.env['crm_lead.crm_lead'].search([]),
#         })

#     @http.route('/crm_lead/crm_lead/objects/<model("crm_lead.crm_lead"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_lead.object', {
#             'object': obj
#         })