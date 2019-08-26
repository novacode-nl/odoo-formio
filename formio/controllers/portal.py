# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        domain = [('user_id', '=', request.env.user.id), ('builder_id.portal', '=', True)]
        values['form_count'] = request.env['formio.form'].sudo().search_count(domain)
        return values

    @http.route(['/my/formio'], type='http', auth="user", website=True)
    def portal_my_formio(self, sortby=None, search=None, search_in='content',  **kw):
        values = self._prepare_portal_layout_values()

        domain = [
            ('user_id', '=', request.env.user.id)
        ]
        order = 'name ASC'
        forms = request.env['formio.form'].sudo().search(domain, order=order)

        values.update({
            'forms': forms, # TODO wrap []
            'page_name': 'formio',
            'default_url': '/my/formio',
        })
        return request.render("formio.portal_my_formio", values)
