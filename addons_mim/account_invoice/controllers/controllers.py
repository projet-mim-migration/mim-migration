# -*- coding: utf-8 -*-
from odoo import http

# class AccountInvoice(http.Controller):
#     @http.route('/account_invoice/account_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice/account_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice.listing', {
#             'root': '/account_invoice/account_invoice',
#             'objects': http.request.env['account_invoice.account_invoice'].search([]),
#         })

#     @http.route('/account_invoice/account_invoice/objects/<model("account_invoice.account_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice.object', {
#             'object': obj
#         })