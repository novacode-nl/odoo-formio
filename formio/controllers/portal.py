# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

from ..models.formio_builder import STATE_CURRENT


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        domain = [('user_id', '=', request.env.user.id), ('builder_id.portal', '=', True)]
        values['form_count'] = request.env['formio.form'].search_count(domain)
        return values

    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)

    @http.route(['/my/formio'], type='http', auth="user", website=True)
    def portal_forms(self, sortby=None, search=None, search_in='content',  **kw):
        values = self._prepare_portal_layout_values()

        domain = [
            ('user_id', '=', request.env.user.id)
        ]
        order = 'create_date DESC'
        forms = request.env['formio.form'].search(domain, order=order)

        # TODO create model (class)method for this?
        domain = [
            ('portal', '=', True),
            ('state', '=', STATE_CURRENT)
        ]
        # TODO order by sequence?
        order = 'name ASC'

        builders_create_form = request.env['formio.builder'].search(domain, order=order)
        values.update({
            'forms': forms,
            'builders_create_form': builders_create_form,
            'page_name': 'formio',
            'default_url': '/my/formio',
        })
        return request.render("formio.portal_my_formio", values)

    @http.route('/my/formio/form/<string:uuid>', type='http', auth='user', website=True)
    def portal_form(self, uuid, **kwargs):
        values = self._prepare_portal_layout_values()
        form = self._get_form(uuid, 'read')
        if not form:
            # TODO website page with message?
            return request.redirect("/")

        # Needed to update language
        context = request.env.context.copy()
        context.update({'lang': request.env.user.lang})
        request.env.context = context

        # Get active languages used in Builder translations.
        query = """
            SELECT
              DISTINCT(fbt.lang_id) AS lang_id
            FROM
              formio_builder_translation AS fbt
              INNER JOIN res_lang AS l ON l.id = fbt.lang_id
            WHERE
              fbt.builder_id = {builder_id}
              AND l.active = True
        """.format(builder_id=form.builder_id.id)

        request.env.cr.execute(query)
        builder_lang_ids = [r[0] for r in request.env.cr.fetchall()]

        # Always include english (en_US).
        domain = ['|', ('id', 'in', builder_lang_ids), ('code', 'in', [request.env.user.lang, 'en_US'])]
        languages = request.env['res.lang'].with_context(active_test=False).search(domain, order='name asc')
        languages = languages.filtered(lambda r: r.id in builder_lang_ids or r.code == 'en_US')

        values = {
            'languages': [], # initialize, otherwise template/view crashes.
            'user': request.env.user,
            'form': form,
            'page_name': 'formio',
        }
        if len(languages) > 1:
            values['languages'] = languages

        return request.render("formio.portal_my_formio_edit", values)

    @http.route(['/my/formio/create/<string:name>'], type='http', auth="user", method=['GET'], website=True)
    def portal_create_form(self, name):
        builder = request.env['formio.builder'].search([('name', '=', name), ('portal', '=', True)], limit=1)
        if not builder:
            # TODO website page with message?
            return request.redirect('/my/formio')
        vals = {
            'builder_id': builder.id,
            'title': builder.title,
            'user_id': request.env.user.id
        }
        form = request.env['formio.form'].create(vals)
        url = '/my/formio/form/{uuid}'.format(uuid=form.uuid)
        return request.redirect(url)

    @http.route(['/my/formio/delete/<string:uuid>'], type='http', auth="user", method=['GET'], website=True)
    def portal_delete_form(self, uuid):
        """ Unlink form. Access rules apply on the unlink method """

        form = request.env['formio.form'].get_form(uuid, 'unlink')
        if not form:
            # TODO call method (website_formio page) with message?
            return request.redirect('/my/formio')
        form.unlink()
        # TODO call method (website_formio page) with message?
        return request.redirect('/my/formio')

    @http.route(['/my/formio/cancel/<string:uuid>'], type='http', auth="user", method=['GET'], website=True)
    def portal_cancel_form(self, uuid):
        """ Cancel form. Access rules apply on the write method """

        form = request.env['formio.form'].get_form(uuid, 'write')
        if not form:
            # TODO call method (website_formio page) with message?
            return request.redirect('/my/formio')
        form.action_cancel()
        # TODO call method (website_formio page) with message?
        return request.redirect('/my/formio')
