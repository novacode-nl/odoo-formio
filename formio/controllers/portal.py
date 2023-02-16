# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging

from odoo import http, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

from ..models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT

from ..models.formio_form import (
    STATE_DRAFT as FORM_STATE_DRAFT,
    STATE_COMPLETE as FORM_STATE_COMPLETE,
)

_logger = logging.getLogger(__name__)


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
            ('state', '=', BUILDER_STATE_CURRENT)
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
        values = {
            'form': form,
            'page_name': 'formio',
        }
        return self._get_page_view_values(form, False, values, 'my_formio', False, **kwargs)

    def _formio_form_new_get_page_view_values(self, builder, **kwargs):
        values = {
            'builder': builder,
            'page_name': 'formio',
        }
        return self._get_page_view_values(builder, False, values, 'my_formio', False, **kwargs)

    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)

    def _redirect_url(self, **kwargs):
        res_model = kwargs.get('res_model')
        res_id = kwargs.get('res_id')
        if res_model and res_id:
            return '/my/formio?res_model=%s&res_id=%s' % (res_model, res_id)
        else:
            return '/my/formio'

    ####################
    # Form - portal list
    ####################

    @http.route(['/my/formio'], type='http', auth="user", website=True)
    def portal_forms(self, sortby=None, search=None, search_in='content',  **kwargs):
        domain = [
            ('user_id', '=', request.env.user.id),
            ('portal_share', '=', True)
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

    ###############################
    # Form - portal create and uuid
    ###############################

    @http.route('/my/formio/form/<string:uuid>', type='http', auth='user', website=True)
    def portal_form(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if not form:
            # TODO website page with message?
            return request.redirect("/")

        values = self._formio_form_get_page_view_values(form, **kwargs)
        return request.render("formio.portal_my_formio_edit", values)

    @http.route(['/my/formio/form/create/<string:name>'], type='http', auth="user", methods=['GET'], website=True)
    def portal_create_form(self, name):
        builder = request.env['formio.builder'].search([('name', '=', name), ('portal', '=', True)], limit=1)
        if not builder:
            redirect_url = self._redirect_url()
            # TODO website page with message?
            return request.redirect(redirect_url)
        vals = {
            'builder_id': builder.id,
            'title': builder.title,
            'user_id': request.env.user.id,
            'partner_id': request.env.user.partner_id.id
        }
        form = request.env['formio.form'].create(vals)
        url = '/my/formio/form/{uuid}'.format(uuid=form.uuid)
        return request.redirect(url)

    @http.route(['/my/formio/form/<string:uuid>/delete'], type='http', auth="user", methods=['GET'], website=True)
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

    @http.route(['/my/formio/form/<string:uuid>/cancel'], type='http', auth="user", methods=['GET'], website=True)
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

    @http.route(['/my/formio/form/<string:uuid>/copy'], type='http', auth="user", methods=['GET'], website=True)
    def portal_copy_form(self, uuid, **kwargs):
        form = request.env['formio.form'].get_form(uuid, 'read')
        redirect_url = self._redirect_url(**kwargs)
        if not form:
            # TODO call method (website_formio page) with message?
            return request.redirect(redirect_url)
        form.action_copy()
        # TODO call method (website_formio page) with message?

        return request.redirect(redirect_url)

    ###################
    # Form - portal new
    ###################

    @http.route('/my/formio/form/new/<string:builder_name>', type='http', auth='user', website=True)
    def portal_form_new(self, builder_name, **kwargs):
        builder = self._get_builder_name(builder_name)
        if not builder:
            msg = 'Form Builder (name) %s: not found' % builder_name
            return request.not_found(msg)
        elif not builder.portal:
            msg = 'Form Builder (name) %s: not published on portal' % builder_name
            return request.not_found(msg)

        values = self._formio_form_new_get_page_view_values(builder, **kwargs)
        return request.render("formio.portal_my_formio_new", values)

    @http.route('/formio/portal/form/new/<string:builder_name>', type='http', auth='user', methods=['GET'], website=True)
    def portal_form_new_root(self, builder_name, **kwargs):
        args = request.httprequest.args
        if args.get('api') == 'getData':
            return self._api_get_data(builder_name)
        else:
            builder = self._get_builder_name(builder_name)
            if not builder:
                msg = 'Form Builder (name) %s: not found' % builder_name
                return request.not_found(msg)
            elif not builder.portal:
                msg = 'Form Builder (name) %s: not published on portal' % builder_name
                return request.not_found(msg)

            values = {
                'languages': builder.languages,
                'builder': builder,
                'formio_builder_uuid': builder.uuid,
                'formio_css_assets': builder.formio_css_assets,
                'formio_js_assets': builder.formio_js_assets,
            }
            return request.render('formio.formio_form_portal_new_embed', values)

    @http.route('/formio/portal/form/new/<string:builder_uuid>/config', type='json', auth='user', website=True)
    def form_new_config(self, builder_uuid, **kwargs):
        builder = self._get_builder_uuid(builder_uuid)
        res = {'schema': {}, 'options': {}, 'params': {}}

        if not builder or builder.state != BUILDER_STATE_CURRENT:
            return res

        if builder.schema:
            res['schema'] = json.loads(builder.schema)
            res['options'] = self._get_form_js_options(builder)
            res['params'] = self._get_form_js_params(builder)

        args = request.httprequest.args
        etl_odoo_config = builder.sudo()._etl_odoo_config(params=args.to_dict())
        res['options'].update(etl_odoo_config.get('options', {}))
        return res

    @http.route('/formio/portal/form/new/<string:builder_uuid>/submission', type='json', auth='user', website=True)
    def form_new_submission(self, builder_uuid, **kwargs):
        builder = self._get_builder_uuid(builder_uuid)

        if not builder:
            _logger.info('formio.builder with UUID %s not found' % builder_uuid)
            # TODO raise or set exception (in JSON resonse) ?
            return

        args = request.httprequest.args
        submission_data = {}
        etl_odoo_data = builder.sudo()._etl_odoo_data(params=args.to_dict())
        submission_data.update(etl_odoo_data)
        return json.dumps(submission_data)

    @http.route('/formio/portal/form/new/<string:builder_uuid>/submit', type='json', auth="user", methods=['POST'], website=True)
    def form_new_submit(self, builder_uuid, **post):
        """ Form submit endpoint

        Note:
        In wizard mode, the submit endpoint shall be changed
        (frontend/JS code) to: /formio/form/<string:uuid>/submit
        """
        builder = self._get_builder_uuid(builder_uuid)

        if not builder:
            # TODO raise or set exception (in JSON resonse) ?
            return

        Form = request.env['formio.form']
        vals = {
            'builder_id': builder.id,
            'title': builder.title,
            'submission_data': json.dumps(post['data']),
            'submission_date': fields.Datetime.now(),
            'submission_user_id': request.env.user.id,
            'user_id': request.env.user.id,
            'portal_share': True
        }

        save_draft = post.get('saveDraft') or (post['data'].get('saveDraft') and not post['data'].get('submit'))

        if save_draft:
            vals['state'] = FORM_STATE_DRAFT
        else:
            vals['state'] = FORM_STATE_COMPLETE

        context = {'tracking_disable': True}
        res = Form.with_context(**context).create(vals)

        if vals.get('state') == FORM_STATE_COMPLETE:
            res.after_submit()
        request.session['formio_last_form_uuid'] = res.uuid
        return {'form_uuid': res.uuid}

    @http.route('/formio/portal/form/new/<string:builder_name>/data')
    def form_new_data(self, builder_name, **kwargs):
        """ Get data dispatch URL.

        DEPRECATED / CHANGE
        ===================
        Use the query string "?api=getData" in URL:
        /formio/portal/form/new/<string:builder_name>?api=getData

        EXAMPLE
        =======
        This example loads data into Select Component, whereby choices
        are the Partner/Contact names with city "Sittard".

        formio configuration (in "Data" tab)
        -------------------------------------
        - Data Source URL: /data
        - Filter Query: model=res.partner&label=name&domain_fields=city&city=Sittard
        """
        msg = "The /data fetching URL %s will be deprecated and work with a minor change in Odoo version 16.0\nMore info on Wiki: %s" % (
            "/formio/portal/form/new/<string:builder_name>/data",
            "https://github.com/novacode-nl/odoo-formio/wiki/Populate-a-Select-Component-data-(options)-with-data-from-Odoo-model.field",
        )
        _logger.warning(msg)
        return self._api_get_data(builder_name)

    ############
    # Misc utils
    ############

    def _api_get_data(self, builder_name):
        """ Get data """
        builder = self._get_builder_name(builder_name)
        if not builder:
            _logger.info('api=getData: Form Builder (name) %s is not found or allowed' % builder_name)
            return []

        args = request.httprequest.args

        model = args.get('model')
        # TODO: formio error?
        if model is None:
            _logger('model is missing in "Data Filter Query"')

        label = args.get('label')
        # TODO: formio error?
        if label is None:
            _logger.error('label is missing in "Data Filter Query"')

        domain = []
        domain_fields = args.getlist('domain_fields')
        # domain_fields_op = args.getlist('domain_fields_operators')

        for domain_field in domain_fields:
            value = args.get(domain_field)

            if value is not None:
                filter = (domain_field, '=', value)
                domain.append(filter)

        if not domain:
            domain = builder._generate_odoo_domain(domain, params=args.to_dict())

        try:
            language = args.get('language')
            if language:
                lang = request.env['res.lang']._from_formio_ietf_code(language)
                model_obj = request.env[model].with_context(lang=lang)
            else:
                model_obj = request.env[model]
            records = model_obj.search_read(domain, [label])
            data = json.dumps([{'id': r['id'], 'label': r[label]} for r in records])
            return data
        except Exception as e:
            # TODO also raise or ensure exception to render in form?
            _logger.error("Exception: %s" % e)

    def _get_builder_uuid(self, builder_uuid):
        return request.env['formio.builder'].get_portal_builder_uuid(builder_uuid)

    def _get_builder_name(self, builder_name):
        return request.env['formio.builder'].get_portal_builder_name(builder_name)

    def _get_form_js_options(self, builder):
        options = {
            'embedded': True,
            'i18n': builder.i18n_translations()
        }

        # language
        Lang = request.env['res.lang']
        if request.context.get('lang'):
            options['language'] = Lang._formio_ietf_code(request.context.get('lang'))
        elif request.env.user.lang:
            options['language'] = Lang._formio_ietf_code(request.env.user.lang)
        else:
            options['language'] = request.env.ref('base.lang_en').formio_ietf_code

        return options

    def _get_form_js_params(self, builder):
        return builder._get_portal_form_js_params()
