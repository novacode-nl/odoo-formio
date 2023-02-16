# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging

from odoo import http, fields
from odoo.http import request

from ..models.formio_builder import \
    STATE_CURRENT as BUILDER_STATE_CURRENT

from ..models.formio_form import \
    STATE_PENDING as FORM_STATE_PENDING, STATE_DRAFT as FORM_STATE_DRAFT, \
    STATE_COMPLETE as FORM_STATE_COMPLETE, STATE_CANCEL as FORM_STATE_CANCEL

_logger = logging.getLogger(__name__)


class FormioPublicController(http.Controller):

    ###############
    # Form - public
    ###############

    @http.route('/formio/public/form/<string:uuid>', type='http', auth='public', website=True)
    def public_form_root(self, uuid, **kwargs):
        form = self._get_public_form(uuid, self._check_public_form())
        if not form:
            msg = 'Form UUID %s' % uuid
            return request.not_found(msg)

        args = request.httprequest.args
        if args.get('api') == 'getData':
            return self._api_get_data(form.builder_id)
        else:
            values = {
                'languages': form.builder_id.languages,
                'form': form,
                'formio_css_assets': form.builder_id.formio_css_assets,
                'formio_js_assets': form.builder_id.formio_js_assets,
            }
            return request.render('formio.formio_form_public_embed', values)

    @http.route('/formio/public/form/<string:form_uuid>/config', type='json', auth='public', website=True)
    def form_config(self, form_uuid, **kwargs):
        form = self._get_public_form(form_uuid, self._check_public_form())
        res = {'schema': {}, 'options': {}, 'params': {}}

        if form and form.builder_id.schema:
            res['schema'] = json.loads(form.builder_id.schema)
            res['options'] = self._get_public_form_js_options(form)
            res['params'] = self._get_public_form_js_params(form.builder_id)

        args = request.httprequest.args
        etl_odoo_config = form.builder_id.sudo()._etl_odoo_config(params=args.to_dict())
        res['options'].update(etl_odoo_config.get('options', {}))
        return res

    @http.route('/formio/public/form/<string:uuid>/submission', type='json', auth='public', website=True)
    def public_form_submission(self, uuid, **kwargs):
        form = self._get_public_form(uuid, self._check_public_form())

        # Submission data
        if form and form.submission_data:
            submission_data = json.loads(form.submission_data)
        else:
            submission_data = {}

        # ETL Odoo data
        if form:
            etl_odoo_data = form.sudo()._etl_odoo_data()
            submission_data.update(etl_odoo_data)

        return json.dumps(submission_data)

    @http.route('/formio/public/form/<string:uuid>/submit', type='json', auth="public", methods=['POST'], website=True)
    def public_form_submit(self, uuid, **post):
        """ POST with ID instead of uuid, to get the model object right away """

        form = self._get_public_form(uuid, self._check_public_form())
        if not form:
            # TODO raise or set exception (in JSON resonse) ?
            return

        vals = {
            'submission_data': json.dumps(post['data']),
            'submission_user_id': request.env.user.id,
            'submission_date': fields.Datetime.now(),
        }

        if post.get('saveDraft') or (post['data'].get('saveDraft') and not post['data'].get('submit')):
            vals['state'] = FORM_STATE_DRAFT
        else:
            vals['state'] = FORM_STATE_COMPLETE

        form.write(vals)

        if vals.get('state') == FORM_STATE_COMPLETE:
            form.after_submit()

    ######################
    # Form - public create
    ######################

    @http.route('/formio/public/form/create/<string:builder_uuid>', type='http', auth='public', methods=['GET'], website=True)
    def public_form_create_root(self, builder_uuid, **kwargs):
        formio_builder = self._get_public_builder(builder_uuid)

        if not formio_builder:
            msg = 'Form Builder UUID %s: not found' % builder_uuid
            return request.not_found(msg)
        elif not formio_builder.public:
            msg = 'Form Builder UUID %s: not public' % builder_uuid
            return request.not_found(msg)
        # elif not formio_builder.state != BUILDER_STATE_CURRENT:
        #     msg = 'Form Builder UUID %s not current/published' % builder_uuid
        #     return request.not_found(msg)

        args = request.httprequest.args
        if args.get('api') == 'getData':
            return self._api_get_data(formio_builder)
        else:
            values = {
                'languages': formio_builder.languages,
                'builder': formio_builder,
                'public_form_create': True,
                'formio_builder_uuid': formio_builder.uuid,
                'formio_css_assets': formio_builder.formio_css_assets,
                'formio_js_assets': formio_builder.formio_js_assets,
            }
            return request.render('formio.formio_form_public_create_embed', values)

    @http.route('/formio/public/form/create/<string:builder_uuid>/config', type='json', auth='public', website=True)
    def public_form_create_config(self, builder_uuid, **kwargs):
        formio_builder = self._get_public_builder(builder_uuid)
        res = {'schema': {}, 'options': {}}

        if not formio_builder or not formio_builder.public or formio_builder.state != BUILDER_STATE_CURRENT:
            return res

        if formio_builder.schema:
            res['schema'] = json.loads(formio_builder.schema)
            res['options'] = self._get_public_create_form_js_options(formio_builder)
            res['params'] = self._get_public_form_js_params(formio_builder)

        args = request.httprequest.args
        etl_odoo_config = formio_builder.sudo()._etl_odoo_config(params=args.to_dict())
        res['options'].update(etl_odoo_config.get('options', {}))

        return res

    @http.route('/formio/public/form/create/<string:builder_uuid>/submit', type='json', auth="public", methods=['POST'], website=True)
    def public_form_create_submit(self, builder_uuid, **post):
        formio_builder = self._get_public_builder(builder_uuid)
        if not formio_builder:
            # TODO raise or set exception (in JSON resonse) ?
            return

        Form = request.env['formio.form']
        vals = {
            'builder_id': formio_builder.id,
            'title': formio_builder.title,
            'public_create': True,
            'public_share': True,
            'submission_data': json.dumps(post['data']),
            'submission_date': fields.Datetime.now(),
            'submission_user_id': request.env.user.id
        }

        save_draft = post.get('saveDraft') or (post['data'].get('saveDraft') and not post['data'].get('submit'))

        if save_draft:
            vals['state'] = FORM_STATE_DRAFT
        else:
            vals['state'] = FORM_STATE_COMPLETE

        context = {'tracking_disable': True}

        if request.env.user._is_public():
            Form = Form.with_company(request.env.user.sudo().company_id)
            res = Form.with_context(**context).sudo().create(vals)
        else:
            res = Form.with_context(**context).create(vals)
        if vals.get('state') == FORM_STATE_COMPLETE:
            res.after_submit()
        request.session['formio_last_form_uuid'] = res.uuid
        return {'form_uuid': res.uuid}

    ########################
    # Form - fetch Odoo data
    ########################

    @http.route('/formio/public/form/create/<string:uuid>/data', type='http', auth='public', website=True)
    def form_data(self, uuid, **kwargs):
        """ Get data from a resource-object.

        DEPRECATED / CHANGE
        ===================
        Use the query string "?api=getData" in URL:
        /formio/public/form/create/<string:uuid>?api=getData

        EXAMPLE
        =======
        This example loads data into Select Component, whereby choices
        are Fleet Vehicle Model with Branc ID 5".

        formio configuration (in "Data" tab)
        -------------------------------------
        - Data Source URL: /data
        - Filter Query: model=fleet.vehicle.model&label=display_name&domain_fields=brand_id&brand_id=5
        """
        msg = "The /data fetching URL %s will be deprecated and work with a minor change in Odoo version 16.0\nMore info on Wiki: %s" % (
            "/formio/public/form/create/<string:uuid>/data",
            "https://github.com/novacode-nl/odoo-formio/wiki/Populate-a-Select-Component-data-(options)-with-data-from-Odoo-model.field",
        )
        _logger.warning(msg)
        return self._api_get_data_builder_uuid(uuid)

    ############
    # Misc utils
    ############

    def _api_get_data_builder_uuid(self, builder_uuid):
        builder = self._get_public_builder(builder_uuid)
        if builder:
            return self._api_get_data(builder)
        else:
            _logger.info('api=getData: Form Builder (uuid) %s is not found or allowed' % builder_uuid)
            return []

    def _api_get_data(self, builder):
        if not builder.public:
            _logger.info('api=getData: Form Builder (uuid) %s is not allowed' % builder.uuid)
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
            # TODO document priority of domain_fields OR domain_api
            domain = builder._generate_odoo_domain(domain, params=args.to_dict())

        _logger.debug("domain: %s" % domain)

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
            _logger.error("Exception: %s" % e)

    def _get_public_form_js_options(self, form):
        options = form._get_js_options()

        Lang = request.env['res.lang']
        language = Lang._formio_ietf_code(request.env.user.lang)
        if language:
            options['language'] = language
            options['i18n'] = form.i18n_translations()
        return options

    def _get_public_create_form_js_options(self, builder):
        options = {
            'public_create': True,
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

    def _get_public_form_js_params(self, builder):
        return builder._get_public_form_js_params()

    def _get_public_form(self, form_uuid, public_share=False):
        return request.env['formio.form'].get_public_form(form_uuid, public_share)

    def _get_public_builder(self, builder_uuid):
        return request.env['formio.builder'].get_public_builder(builder_uuid)

    def _check_public_form(self):
        return request._uid == request.env.ref('base.public_user').id or request._uid

    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)
