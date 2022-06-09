# -*- coding: utf-8 -*-
# from odoo.http import request
from odoo import http


class Rank(http.Controller):
    @http.route('/custom/addons/rank/rank_landing_hero', auth='user', type='json')
    def index(self):
        print('-----------------------------------------')
        print('=========================================')
        return {'html': """
                    Hello, world
                    """}

    # @http.route('/rank/rank/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('rank.listing', {
    #         'root': '/rank/rank',
    #         'objects': http.request.env['rank.rank'].search([]),
    #     })

    # @http.route('/rank/rank/objects/<model("rank.rank"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('rank.object', {
    #         'object': obj
    #     })


# class OnboardingController(http.Controller):

#     @http.route('/account/account_invoice_onboarding', auth='user', type='json')
#     def account_invoice_onboarding(self):
#         """ Returns the `banner` for the account invoice onboarding panel.
#             It can be empty if the user has closed it or if he doesn't have
#             the permission to see it. """

#         company = request.env.company
#         if not request.env.is_admin() or \
#                 company.account_invoice_onboarding_state == 'closed':
#             return {}

#         return {
#             'html': request.env.ref('account.account_invoice_onboarding_panel')._render({
#                 'company': company,
#                 'state': company.get_and_update_account_invoice_onboarding_state()
#             })
#         }
