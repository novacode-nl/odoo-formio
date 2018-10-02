# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError


class Formio(http.Controller):

    # Builder
    @http.route('/formio/builder/<int:builder_id>', type='http', auth='user', website=True)
    def builder_edit(self, builder_id, **kwargs):
        builder = request.env['formio.builder'].browse(builder_id)
        values = {
            'builder_id': builder_id,
            'builder_name': builder.name,
            'builder_title': builder.title,
        }
        return request.render('formio.formio_builder', values)

    @http.route('/formio/builder/schema/<int:builder_id>', type='json', auth='user', website=True)
    def builder_schema(self, builder_id, **kwargs):
        builder = request.env['formio.builder'].browse(builder_id)
        if builder and builder.schema:
            return builder.schema
        else:
            return {}

    @http.route('/formio/builder/save/<model("formio.builder"):builder>', type='json', auth="user", methods=['POST'], website=True)
    def builder_save(self, builder, **post):
        if not 'builder_id' in post or int(post['builder_id']) != builder.id:
            # TODO raise or set exception (in JSON resonse) ?
            return
        
        schema = json.dumps(post['schema'])
        builder.write({'schema': schema})

    # Form
    @http.route('/formio/form/<int:form_id>', type='http', auth='user', website=True)
    def form_edit(self, form_id, **kwargs):
        form = request.env['formio.form'].browse(form_id)
        values = {
            'form_id': form_id,
            'form_name': form.name,
            'form_title': form.title,
        }
        return request.render('formio.formio_form', values)

    @http.route('/formio/form/schema/<int:form_id>', type='json', auth='user', website=True)
    def form_schema(self, form_id, **kwargs):
        form = request.env['formio.form'].browse(form_id)
        if form and form.builder_id.schema:
            return form.builder_id.schema
        else:
            return {}

    @http.route('/formio/form/data/<int:form_id>', type='json', auth='user', website=True)
    def form_data(self, form_id, **kwargs):
        form = request.env['formio.form'].browse(form_id)
        if form and form.submission_data:
            return form.submission_data
        else:
            return {}

    @http.route('/formio/form/submit/<model("formio.form"):form>', type='json', auth="user", methods=['POST'], website=True)
    def form_submit(self, form, **post):
        if not 'form_id' in post or int(post['form_id']) != form.id:
            # TODO raise or set exception (in JSON resonse) ?
            return
        
        vals = {
            'submission_data': json.dumps(post['data']),
            'submission_user_id': request.env.user.id,
            'submission_date': fields.Datetime.now(),
        }
        form.write(vals)
