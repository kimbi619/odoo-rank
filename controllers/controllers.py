# -*- coding: utf-8 -*-
# from odoo import http


# class Rank(http.Controller):
#     @http.route('/rank/rank/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rank/rank/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rank.listing', {
#             'root': '/rank/rank',
#             'objects': http.request.env['rank.rank'].search([]),
#         })

#     @http.route('/rank/rank/objects/<model("rank.rank"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rank.object', {
#             'object': obj
#         })
