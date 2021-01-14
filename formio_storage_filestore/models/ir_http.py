# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import pdb
import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _authenticate(cls, auth_method='user'):
        if request.httprequest.path == '/formio/storage/filestore':
            log = {
                'request_path': request.httprequest.path,
                'auth_method': auth_method,
                'request_user_id': request._context.get('uid')
            }
            _logger.debug(log)

            if auth_method == 'user' and request._context.get('uid'):
                auth_method = super(IrHttp, cls)._authenticate(auth_method)
                return auth_method
            else:
                _logger.debug('Allow public /formio/storage/filestore , become: auth=public')
                return 'public'
        else:
            return super(IrHttp, cls)._authenticate(auth_method)
