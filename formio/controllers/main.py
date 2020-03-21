# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from collections import deque
import json
import logging

from flectra import http, fields
from flectra.http import request

from ..models.formio_builder import \
    STATE_CURRENT as BUILDER_STATE_CURRENT, STATE_OBSOLETE as BUILDER_STATE_OBSOLETE

from ..models.formio_form import \
    STATE_DRAFT as FORM_STATE_DRAFT, STATE_COMPLETE as FORM_STATE_COMPLETE, STATE_CANCEL as FORM_STATE_CANCEL

_logger = logging.getLogger(__name__)


class FormioController(http.Controller):

    # Builder
    @http.route('/formio/builder/<int:builder_id>', type='http', auth='user', website=True)
    def builder_root(self, builder_id, **kwargs):
        if not request.env.user.has_group('formio.group_formio_admin'):
            # TODO Render template with message?
            return request.redirect("/")

        # Needed to update language
        context = request.env.context.copy()
        context.update({'lang': request.env.user.lang})
        request.env.context = context

        builder = request.env['formio.builder'].browse(builder_id)
        values = {
            'builder': builder,
            'formio_css_assets': builder.formio_css_assets,
            'formio_js_assets': builder.formio_js_assets,
        }
        return request.render('formio.formio_builder_embed', values)

    @http.route('/formio/builder/options/<int:builder_id>', type='json', auth='user', website=True)
    def builder_options(self, builder_id, **kwargs):
        if not request.env.user.has_group('formio.group_formio_admin'):
            return
        builder = request.env['formio.builder'].browse(builder_id)
        if builder:
            options = self._prepare_builder_options(builder)
        else:
            options = {}
        return json.dumps(options)

    @http.route('/formio/builder/schema/<int:builder_id>', type='json', auth='user', website=True)
    def builder_schema(self, builder_id, **kwargs):
        if not request.env.user.has_group('formio.group_formio_admin'):
            return
        
        builder = request.env['formio.builder'].browse(builder_id)
        if builder and builder.schema:
            return builder.schema
        else:
            return {}

    @http.route('/formio/builder/save/<model("formio.builder"):builder>', type='json', auth="user", methods=['POST'], website=True)
    def builder_save(self, builder, **post):
        if not request.env.user.has_group('formio.group_formio_admin'):
            return
        
        if not 'builder_id' in post or int(post['builder_id']) != builder.id:
            return
        
        schema = json.dumps(post['schema'])
        builder.write({'schema': schema})

    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)

    # Form
    @http.route('/formio/form/<string:uuid>/root', type='http', auth='user', website=True)
    def form_root(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if not form:
            # TODO Render template with message?
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
            'form': form,
            'formio_css_assets': form.builder_id.formio_css_assets,
            'formio_js_assets': form.builder_id.formio_js_assets,
        }
        if len(languages) > 1:
            values['languages'] = languages
        return request.render('formio.formio_form_embed', values)

    @http.route('/formio/form/<string:uuid>/schema', type='json', auth='user', website=True)
    def form_schema(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if form and form.builder_id.schema:
            return form.builder_id.schema
        else:
            return {}

    def _prepare_builder_options(self, builder):
        options = {}

        if builder.state in [BUILDER_STATE_CURRENT, BUILDER_STATE_OBSOLETE]:
            options['readOnly'] = True
        return options

    def _prepare_form_options(self, form):
        options = {}
        i18n = {}
        context = request.env.context
        Lang  = request.env['res.lang']

        if form.state in [FORM_STATE_COMPLETE, FORM_STATE_CANCEL]:
            options['readOnly'] = True

            if form.builder_id.view_as_html:
                options['renderMode'] = 'html'
                options['viewAsHtml'] = True # backwards compatible (version < 4.x)?

        lang = Lang._lang_get(request.env.user.lang)
        options['language'] = lang.iso_code

        # Formio GUI/API translations
        if form.builder_id.formio_version_id.translations:
            for trans in form.builder_id.formio_version_id.translations:
                if trans.lang_id.iso_code not in i18n:
                    i18n[trans.lang_id.iso_code] = {trans.property: trans.value}
                else:
                    i18n[trans.lang_id.iso_code][trans.property] = trans.value

        # Form Builder translations (labels etc).
        # These could override the former GUI/API translations, but
        # that's how the Javascript API works.
        for trans in form.builder_id.translations:
            if trans.lang_id.iso_code not in i18n:
                i18n[trans.lang_id.iso_code] = {trans.source: trans.value}
            else:
                i18n[trans.lang_id.iso_code][trans.source] = trans.value
            options['i18n'] = i18n

        return options

    @http.route('/formio/form/<string:uuid>/options', type='json', auth='user', website=True)
    def form_options(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if form:
            options = self._prepare_form_options(form)
        else:
            options = {}
        return json.dumps(options)

    @http.route('/formio/form/<string:uuid>/submission', type='json', auth='user', website=True)
    def form_submission(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if form and form.submission_data:
            return form.submission_data
        else:
            return {}

    @http.route('/formio/form/<string:uuid>/submit', type='json', auth="user", methods=['POST'], website=True)
    def form_submit(self, uuid, **post):
        """ POST with ID instead of uuid, to get the model object right away """

        form = self._get_form(uuid, 'write')
        if not form:
            # TODO raise or set exception (in JSON resonse) ?
            return
        
        vals = {
            'submission_data': json.dumps(post['data']),
            'submission_user_id': request.env.user.id,
            'submission_date': fields.Datetime.now(),
        }

        if post['data'].get('saveDraft') and not post['data'].get('submit'):
            vals['state'] = FORM_STATE_DRAFT
        else:
            vals['state'] = FORM_STATE_COMPLETE

        form.write(vals)

    @http.route('/formio/form/<string:uuid>/data', type='http', auth='user', website=True)
    def form_data(self, uuid, **kwargs):
        """ Get data from a resource-object.

        EXAMPLE
        =======
        This example loads data into Select Component, whereby choices
        are the Partner/Contact names with city "Sittard".

        Form.io configuration (in "Data" tab)
        -------------------------------------
        - Data Source URL: data
        - Filter Query: model=res.partner&label=name&domain_fields=city&city=Sittard
        """

        form = self._get_form(uuid, 'read')
        if not form:
            return
        
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

        _logger.debug("domain: %s" % domain)

        try:
            records = request.env[model].search_read(domain, [label])
            data = json.dumps([{'id': r['id'], 'label': r[label]} for r in records])
            return data
        except Exception as e:
            _logger.error("Exception: %s" % e)

    @http.route('/formio/form/<string:uuid>/res_data', type='http', auth='user', website=True)
    def form_res_data(self, uuid, **kwargs):
        """ Get data from a linked resource-object (by: res_model_id, res_id),

        This also traverses relations.

        EXAMPLE
        =======
        This example loads data into Select Component whereby choices
        are the product-names from a Sale Order.
        The Form(Builder) has the "Resource Model" set to "Quotation" (i.e. sale.order).

        Form.io configuration (in "Data" tab)
        -------------------------------------
        - Data Source URL: res_data
        - Filter Query: field=order_line.product_id&label=name
        """

        form = self._get_form(uuid, 'read')
        if not form:
            return

        args = request.httprequest.args

        field = args.get('field')
        # TODO: formio error?
        if field is None:
            _logger('field is missing in "Data Filter Query"')

        label = args.get('label')
        # TODO: formio error?
        if label is None:
            _logger.error('label is missing in "Data Filter Query"')

        try:
            record = request.env[form.res_model_id.model].browse(form.res_id)

            fields = deque(args.get('field').split('.'))
            res_data = []
            while fields:
                _field = fields.popleft()

                if not res_data or not isinstance(res_data.ids, list):
                    res_data = getattr(record, _field)
                elif isinstance(res_data, list):
                    res_data = [get_attr(r, _field) for r in res_data]

            data = json.dumps([{'id': r['id'], 'label': r[label]} for r in res_data])
            return data
        except Exception as e:
            _logger.error("Exception: %s" % e)
