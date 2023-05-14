# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import requests

from odoo import http
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class FormioRecaptchaController(http.Controller):

    @http.route('/formio/component/recaptcha', type='json', auth="none", methods=['POST'], website=True)
    def verification(self, **post):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        secret = request.env['ir.config_parameter'].sudo().get_param('recaptcha_private_key')
        data = {
            'secret': secret,
            'response': post['token']
        }
        response = requests.post(url, data=data)
        if response:
            resp = response.json()
            _logger.info('reCAPTCHA response: %s' % resp)
            return resp
        else:
            return {'success': False}
