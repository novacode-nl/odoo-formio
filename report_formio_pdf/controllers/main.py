# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from collections import deque
import json
import logging

from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


class FormioController(http.Controller):
    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)

    @http.route('/formio/form/<string:uuid>/title', type='json', auth='user', website=True)
    def form_title(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if form and form.title:
            return form.title
        else:
            return {}