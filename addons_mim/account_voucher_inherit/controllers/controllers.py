# -*- coding: utf-8 -*-
from odoo import http

# class AccountVoucherInherit(http.Controller):
#     @http.route('/account_voucher_inherit/account_voucher_inherit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_voucher_inherit/account_voucher_inherit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_voucher_inherit.listing', {
#             'root': '/account_voucher_inherit/account_voucher_inherit',
#             'objects': http.request.env['account_voucher_inherit.account_voucher_inherit'].search([]),
#         })

#     @http.route('/account_voucher_inherit/account_voucher_inherit/objects/<model("account_voucher_inherit.account_voucher_inherit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_voucher_inherit.object', {
#             'object': obj
#         })