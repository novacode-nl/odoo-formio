# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from odoo import http, fields
from odoo.http import request
from odoo.exceptions import ValidationError

def form_by_slug(slug):
    form = request.env['formio.form'].search([('slug', '=', slug)], limit=1)
    return form


class Formio(http.Controller):

    # Builder
    @http.route('/formio/builder/<int:builder_id>', type='http', auth='user', website=True)
    def builder_edit(self, builder_id, **kwargs):
        if not request.env.user.has_group('formio.group_formio_manager'):
            return request.redirect("/")
        
        builder = request.env['formio.builder'].browse(builder_id)
        values = {
            'builder_id': builder_id,
            'builder_name': builder.name,
            'builder_title': builder.title,
            'act_window_url': builder.act_window_url
        }
        return request.render('formio.formio_builder', values)

    @http.route('/formio/builder/schema/<int:builder_id>', type='json', auth='user', website=True)
    def builder_schema(self, builder_id, **kwargs):
        if not request.env.user.has_group('formio.group_formio_manager'):
            return
        
        builder = request.env['formio.builder'].browse(builder_id)
        if builder and builder.schema:
            return builder.schema
        else:
            return {}

    @http.route('/formio/builder/save/<model("formio.builder"):builder>', type='json', auth="user", methods=['POST'], website=True)
    def builder_save(self, builder, **post):
        if not request.env.user.has_group('formio.group_formio_manager'):
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

        # form = request.env['formio.form'].search([('slug', '=', slug)])
        form = form_by_slug(slug)
        values = {
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
        
        # form = request.env['formio.form'].browse(form_id)
        form = form_by_slug(slug)
        if form and form.builder_id.schema:
            return form.builder_id.schema
        else:
            return {}

    @http.route('/formio/form/data/<string:slug>', type='json', auth='user', website=True)
    def form_data(self, slug, **kwargs):
        if not request.env.user.has_group('formio.group_formio_user'):
            return
        
        # form = request.env['formio.form'].browse(form_id)
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
