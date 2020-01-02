# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

from ..models.formio_builder import STATE_CURRENT


class FormioCustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(FormioCustomerPortal, self)._prepare_portal_layout_values()
        domain = [('user_id', '=', request.env.user.id), ('builder_id.portal', '=', True)]
        values['form_count'] = request.env['formio.form'].search_count(domain)
        return values

    def _formio_form_prepare_portal_layout_values(self, **kwargs):
        values = super(FormioCustomerPortal, self)._prepare_portal_layout_values()

        # TODO create model (class)method for this?
        domain = [
            ('portal', '=', True),
            ('formio_res_model_id', '=', False),
            ('state', '=', STATE_CURRENT)
        ]
        # TODO order by sequence?
        order = 'name ASC'
        builders_create_form = request.env['formio.builder'].search(domain, order=order)
        values.update({
            'builders_create_form': builders_create_form,
            'page_name': 'formio',
            'default_url': '/my/formio'
        })

        # Forms
        res_model = kwargs.get('res_model')
        res_id = kwargs.get('res_id')
        if res_model and res_id:
            domain = [
                ('res_model', '=', res_model),
                ('res_id', '=', res_id),
                ('user_id', '=', request.env.user.id),
                ('builder_id.portal', '=', True)
            ]
            forms = request.env['formio.form'].search(domain)
            if forms:
                values['res_model'] = res_model
                values['res_id'] = res_id
                values['res_name'] = forms[0].res_id
                values['form_count'] = len(forms)
        else:
            domain = [('user_id', '=', request.env.user.id), ('builder_id.portal', '=', True)]
            values['form_count'] = request.env['formio.form'].search_count(domain)
        return values

    def _formio_form_get_page_view_values(self, form, **kwargs):
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

        return self._get_page_view_values(form, False, values, 'my_formio', False, **kwargs)

    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)

    def _redirect_url(self, **kwargs):
        res_model = kwargs.get('res_model')
        res_id = kwargs.get('res_id')
        if res_model and res_id:
            return '/my/formio?res_model=%s&res_id=%s' % (res_model, res_id)
        else:
            return '/my/formio'

    @http.route(['/my/formio'], type='http', auth="user", website=True)
    def portal_forms(self, sortby=None, search=None, search_in='content',  **kwargs):
        domain = [
            ('user_id', '=', request.env.user.id),
            ('builder_id.portal', '=', True)
        ]
        res_model = kwargs.get('res_model')
        res_id = kwargs.get('res_id')
        if res_model and res_id:
            domain.append(('res_model', '=', res_model))
            domain.append(('res_id', '=', res_id))
        
        order = 'create_date DESC'
        forms = request.env['formio.form'].search(domain, order=order)

        values = self._formio_form_prepare_portal_layout_values(**kwargs)
        values['forms'] = forms
        return request.render("formio.portal_my_formio", values)

    @http.route('/my/formio/form/<string:uuid>', type='http', auth='user', website=True)
    def portal_form(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if not form:
            # TODO website page with message?
            return request.redirect("/")

        values = self._formio_form_get_page_view_values(form, **kwargs)
        return request.render("formio.portal_my_formio_edit", values)

    @http.route(['/my/formio/create/<string:name>'], type='http', auth="user", method=['GET'], website=True)
    def portal_create_form(self, name):
        builder = request.env['formio.builder'].search([('name', '=', name), ('portal', '=', True)], limit=1)
        if not builder:
            redirect_url = self._redirect_url()
            # TODO website page with message?
            return request.redirect(redirect_utl)
        vals = {
            'builder_id': builder.id,
            'title': builder.title,
            'user_id': request.env.user.id
        }
        form = request.env['formio.form'].create(vals)
        url = '/my/formio/form/{uuid}'.format(uuid=form.uuid)
        return request.redirect(url)

    @http.route(['/my/formio/delete/<string:uuid>'], type='http', auth="user", method=['GET'], website=True)
    def portal_delete_form(self, uuid, **kwargs):
        """ Unlink form. Access rules apply on the unlink method """

        form = request.env['formio.form'].get_form(uuid, 'unlink')
        redirect_url = self._redirect_url(**kwargs)
        if not form:
            # TODO call method (website_formio page) with message?
            return request.redirect(redirect_url)
        form.unlink()
        # TODO call method (website_formio page) with message?

        return request.redirect(redirect_url)

    @http.route(['/my/formio/cancel/<string:uuid>'], type='http', auth="user", method=['GET'], website=True)
    def portal_cancel_form(self, uuid, **kwargs):
        """ Cancel form. Access rules apply on the write method """

        form = request.env['formio.form'].get_form(uuid, 'write')
        redirect_url = self._redirect_url(**kwargs)
        if not form:
            # TODO call method (website_formio page) with message?
            return request.redirect(redirect_url)
        form.action_cancel()
        # TODO call method (website_formio page) with message?
        return request.redirect(redirect_url)
