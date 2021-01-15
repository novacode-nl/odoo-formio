# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging
import os

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _authenticate_formio_storage_filestore(cls, auth_method):
        log = {
            'request_path': request.httprequest.path,
            'auth_method': auth_method,
            'request_user_id': request._context.get('uid')
        }
        _logger.info(log)

        if auth_method == 'user' and request._context.get('uid'):
            return super(IrHttp, cls)._authenticate(auth_method)
        else:
            # Security measurement for public POST/uploads,
            # because CSRF is disabled (needed) for this endpoint.
            base_url = request.httprequest.args.get('baseUrl')
            if '/formio/public/form/create' in base_url:
                uuid = os.path.basename(os.path.normpath(base_url))
                domain = [('uuid', '=', uuid), ('public', '=', True)]
                builder = request.env['formio.builder'].sudo().search(domain)
                if builder:
                    _logger.info('Allow public /formio/storage/filestore with baseUrl %s (become: auth=public)' % base_url)
                    return 'public'
            elif '/formio/public/form/' in base_url:
                uuid = os.path.basename(os.path.normpath(base_url))
                domain = [('uuid', '=', uuid), ('public', '=', True)]
                form = request.env['formio.form'].sudo().search(domain)
                if form:
                    _logger.info('Allow public /formio/storage/filestore with baseUrl %s (become: auth=public)' % base_url)
                    return 'public'
            # Applies if above doesn't
            return False

    @classmethod
    def _authenticate(cls, auth_method='user'):
        if request.httprequest.path == '/formio/storage/filestore':
            res = cls._authenticate_formio_storage_filestore(auth_method)
            if res:
                return res
            else:
                return super(IrHttp, cls)._authenticate(auth_method)
        else:
            return super(IrHttp, cls)._authenticate(auth_method)
