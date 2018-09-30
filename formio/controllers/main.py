# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.


import json

from odoo import http
from odoo.http import request


class Formio(http.Controller):

    @http.route('/formio/builder/<int:builder_id>', type='http', auth='user', website=True)
    def builder_edit(self, builder_id, **kwargs):
        builder = request.env['formio.builder'].browse(builder_id)
        values = {
            'builder_name': builder.name,
            'builder_id': builder_id,
        }
        return request.render('formio.formio_builder', values)

    @http.route('/formio/builder/schema/<int:builder_id>', type='json', auth='user', website=True)
    def builder_schema(self, builder_id, **kwargs):
        builder = request.env['formio.builder'].browse(builder_id)
        if builder and builder.schema:
            return builder.schema
        else:
            return {}

    @http.route('/formio/builder/post/<model("formio.builder"):builder>', type='json', auth="user", methods=['POST'], website=True)
    def builder_save(self, builder, **post):
        if not 'builder_id' in post or int(post['builder_id']) != builder.id:
            # TODO raise or set exception (in JSON resonse) ?
            return
        
        schema = json.dumps(post['schema'])
        builder.write({'schema': schema})
