# -*- coding: utf-8 -*-
from odoo import http

# class DashBoard(http.Controller):
#     @http.route('/dash_board/dash_board/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dash_board/dash_board/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dash_board.listing', {
#             'root': '/dash_board/dash_board',
#             'objects': http.request.env['dash_board.dash_board'].search([]),
#         })

#     @http.route('/dash_board/dash_board/objects/<model("dash_board.dash_board"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dash_board.object', {
#             'object': obj
#         })