# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LicenseController(http.Controller):

    @http.route('/formio/license', type='http', auth='public', csrf=False)
    def license(self, **kwargs):
        domain = [
            ('active', '=', True)
        ]
        licenses = request.env['formio.license'].search(domain)
        res = {
            'licenses': licenses.mapped('key'),
            'language': request.env.context['lang']
        }
        return request.make_json_response(res)
