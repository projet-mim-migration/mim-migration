# -*- coding: utf-8 -*-
from odoo import http

# class AccountBankStatementSecurity(http.Controller):
#     @http.route('/account_bank_statement_security/account_bank_statement_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_bank_statement_security/account_bank_statement_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_bank_statement_security.listing', {
#             'root': '/account_bank_statement_security/account_bank_statement_security',
#             'objects': http.request.env['account_bank_statement_security.account_bank_statement_security'].search([]),
#         })

#     @http.route('/account_bank_statement_security/account_bank_statement_security/objects/<model("account_bank_statement_security.account_bank_statement_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_bank_statement_security.object', {
#             'object': obj
#         })