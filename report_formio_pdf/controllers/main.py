# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging

from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)

formats = {
    'A0': {
        'unit': 'mm',
        'size': [841, 1189]
    },
    'A1': {
        'unit': 'mm',
        'size': [594, 841]
    },
    'A2': {
        'unit': 'mm',
        'size': [420, 594]
    },
    'A3': {
        'unit': 'mm',
        'size': [297, 420]
    },
    'A4': {
        'unit': 'mm',
        'size': [210, 297]
    },
    'A5': {
        'unit': 'mm',
        'size': [148, 210]
    },
    'A6': {
        'unit': 'mm',
        'size': [105, 148]
    },
    'A7': {
        'unit': 'mm',
        'size': [74, 105]
    },
    'A8': {
        'unit': 'mm',
        'size': [52, 74]
    },
    'A9': {
        'unit': 'mm',
        'size': [37, 52]
    },
    'B0': {
        'unit': 'mm',
        'size': [1000, 1414]
    },
    'B1': {
        'unit': 'mm',
        'size': [707, 1000]
    },
    'B2': {
        'unit': 'mm',
        'size': [500, 707]
    },
    'B3': {
        'unit': 'mm',
        'size': [353, 500]
    },
    'B4': {
        'unit': 'mm',
        'size': [250, 353]
    },
    'B5': {
        'unit': 'mm',
        'size': [176, 250]
    },
    'B6': {
        'unit': 'mm',
        'size': [125, 176]
    },
    'B7': {
        'unit': 'mm',
        'size': [88, 125]
    },
    'B8': {
        'unit': 'mm',
        'size': [62, 88]
    },
    'B9': {
        'unit': 'mm',
        'size': [33, 62]
    },
    'B10': {
        'unit': 'mm',
        'size': [31, 44]
    },
    'C5E': {
        'unit': 'mm',
        'size': [163, 229]
    },
    'Comm10E': {
        'unit': 'mm',
        'size': [105, 241]
    },
    'DLE': {
        'unit': 'mm',
        'size': [110, 220]
    },
    'Executive': {
        'unit': 'mm',
        'size': [190.5, 254]
    },
    'Folio': {
        'unit': 'mm',
        'size': [210, 330]
    },
    'Ledger': {
        'unit': 'mm',
        'size': [431.8, 279.4]
    },
    'Legal': {
        'unit': 'mm',
        'size': [215.9, 355.6]
    },
    'Letter': {
        'unit': 'mm',
        'size': [215.9, 279.4]
    },
    'Tabloid': {
        'unit': 'mm',
        'size': [279.4, 431.8]
    },
}

class FormioController(http.Controller):
    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)

    def _prepare_form_paperformat(self):
        result = {}
        pf = request.env.user.company_id.paperformat_id

        # Get the right landscape
        landscape = 'p' if pf.orientation == 'Portrait' else 'l'

        # Check for paper format
        if pf.format in formats:
            result['format'] = formats[pf.format]
        elif pf.format == 'custom':
            result['format'] = {
                'unit': 'mm',
                'size': [pf.page_width, pf.page_height]
            }
        else:
            result['format'] = formats['A4']

        result['orientation'] = landscape
        result['margin_top'] = 10
        result['margin_bottom'] = 10
        result['margin_left'] = pf.margin_left
        result['margin_right'] = pf.margin_right

        return result

    @http.route('/formio/form/<string:uuid>/title', type='json', auth='user', website=True)
    def form_title(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')
        if form and form.title:
            return form.title
        else:
            return {}

    @http.route('/formio/form/<string:uuid>/paperformat', type='json', auth='user', website=True)
    def form_paperformat(self, uuid, **kwargs):
        form = self._get_form(uuid, 'read')

        if form:
            paperformat = self._prepare_form_paperformat()
        else:
            paperformat = {}
        return json.dumps(paperformat)