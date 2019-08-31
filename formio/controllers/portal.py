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

        # TODO create model (class)method for this?
        domain = [
            ('portal', '=', True)
        ]
        # TODO order by sequence?
        order = 'name ASC'

        builders_create_form = request.env['formio.builder'].sudo().search(domain, order=order)
        values.update({
            'forms': forms,
            'builders_create_form': builders_create_form,
            'page_name': 'formio',
            'default_url': '/my/formio',
        })
        return request.render("formio.portal_my_formio", values)

    @http.route(['/my/formio/create/<string:name>'], type='http', auth="user", method=['GET'], website=True)
    def portal_create_form(self, name):
        builder = request.env['formio.builder'].search([('name', '=', name), ('portal', '=', True)], limit=1)
        if not builder:
            # TODO website page with message?
            return request.redirect('/my/formio')
        vals = {
            'builder_id': builder.id,
            'user_id': request.env.user.id
        }
        form = request.env['formio.form'].create(vals)
        url = '/formio/form/{uuid}'.format(uuid=form.uuid)
        return request.redirect(url)
