# -*- coding: utf-8 -*-
from odoo import http

# class ConfirmedApproved(http.Controller):
#     @http.route('/confirmed_approved/confirmed_approved/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/confirmed_approved/confirmed_approved/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('confirmed_approved.listing', {
#             'root': '/confirmed_approved/confirmed_approved',
#             'objects': http.request.env['confirmed_approved.confirmed_approved'].search([]),
#         })

#     @http.route('/confirmed_approved/confirmed_approved/objects/<model("confirmed_approved.confirmed_approved"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('confirmed_approved.object', {
#             'object': obj
#         })