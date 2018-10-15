# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from collections import deque
import json
import logging

from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

def form_by_slug(slug):
    form = request.env['formio.form'].search([('slug', '=', slug)], limit=1)
    return form


class Formio(http.Controller):

    # Builder
    @http.route('/formio/builder/<int:builder_id>', type='http', auth='user', website=True)
    def builder_edit(self, builder_id, **kwargs):
        if not request.env.user.has_group('formio.group_formio_admin'):
            return request.redirect("/")
        
        builder = request.env['formio.builder'].browse(builder_id)
        values = {
            'builder': builder,
            'formio_css_assets': builder.formio_css_assets,
            'formio_js_assets': builder.formio_js_assets,
            'builder_id': builder_id,
            'builder_name': builder.name,
            'builder_title': builder.title,
            'act_window_url': builder.act_window_url,
        }
        return request.render('formio.formio_builder', values)

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

    # Form
    @http.route('/formio/form/<string:slug>', type='http', auth='user', website=True)
    def form_edit(self, slug, **kwargs):
        if not request.env.user.has_group('formio.group_formio_user'):
            return request.redirect("/")

        form = form_by_slug(slug)
        scheme = request.httprequest.environ['wsgi.url_scheme']
        host = request.httprequest.environ['HTTP_HOST']
        base_url = scheme + '://' + host

        values = {
            'base_url': base_url,
            'formio_css_assets': form.builder_id.formio_css_assets,
            'formio_js_assets': form.builder_id.formio_js_assets,
            'slug': form.slug,
            'id': form.id,
            'name': form.name,
            'title': form.title,
            'act_window_url': form.act_window_url,
            'res_act_window_url': form.res_act_window_url,
            'res_name': form.res_name,
            'res_info': form.res_info,
        }
        return request.render('formio.formio_form', values)

    @http.route('/formio/form/schema/<string:slug>', type='json', auth='user', website=True)
    def form_schema(self, slug, **kwargs):
        if not request.env.user.has_group('formio.group_formio_user'):
            return
        
        form = form_by_slug(slug)
        if form and form.builder_id.schema:
            return form.builder_id.schema
        else:
            return {}

    @http.route('/formio/form/submission/<string:slug>', type='json', auth='user', website=True)
    def form_submission(self, slug, **kwargs):
        if not request.env.user.has_group('formio.group_formio_user'):
            return
        
        form = form_by_slug(slug)
        if form and form.submission_data:
            return form.submission_data
        else:
            return {}

    @http.route('/formio/form/submit/<string:slug>', type='json', auth="user", methods=['POST'], website=True)
    def form_submit(self, slug, **post):
        """ POST with ID instead of slug, to get the model object right away """
        if not request.env.user.has_group('formio.group_formio_user'):
            return

        form = form_by_slug(slug)
        if not form:
            # TODO raise or set exception (in JSON resonse) ?
            return
        
        vals = {
            'submission_data': json.dumps(post['data']),
            'submission_user_id': request.env.user.id,
            'submission_date': fields.Datetime.now(),
        }
        form.write(vals)

    @http.route('/formio/form/data/<string:slug>', type='http', auth='user', website=True)
    def form_data(self, slug, **kwargs):
        """ Get data from a resource-object.

        EXAMPLE
        =======
        This example loads data into Select Component, whereby choices
        are the Partner/Contact names with city "Sittard".

        Form.io configuration (in "Data" tab)
        -------------------------------------
        - Data Source URL: /formio/form/res_data
        - Filter Query: model=res.partner&label=name&domain_fields=function&city=Sittard
        """
        if not request.env.user.has_group('formio.group_formio_user'):
            return

        form = form_by_slug(slug)
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

    @http.route('/formio/form/res_data/<string:slug>', type='http', auth='user', website=True)
    def form_res_data(self, slug, **kwargs):
        """ Get data from a linked resource-object (by: res_model_id, res_id),

        This also traverses relations.

        EXAMPLE
        =======
        This example loads data into Select Component whereby choices
        are the product-names from a Sale Order.
        The Form(Builder) has the "Resource Model" set to "Quotation" (i.e. sale.order).

        Form.io configuration (in "Data" tab)
        -------------------------------------
        - Data Source URL: /formio/form/res_data
        - Filter Query: field=order_line.product_id&label=name
        """

        if not request.env.user.has_group('formio.group_formio_user'):
            return

        form = form_by_slug(slug)
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
