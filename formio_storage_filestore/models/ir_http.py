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
    def _authenticate(cls, endpoint):
        """
        :param endpoint str: the endpoint config, for example (endpoint.__dict_):
            {'method': <bound method FormioStorageFilestoreController.form_file_post of <odoo.addons.formio_storage_filestore.controllers.main.FormioStorageFilestoreController object at 0x7fa358108520>>,
             'original': <function FormioStorageFilestoreController.form_file_post at 0x7fa35990a1f0>,
             'routing': {'type': 'http', 'auth': 'user', 'methods': ['POST'], 'routes': ['/formio/storage/filestore'], 'csrf': False},
             'arguments': {}
            }
        """
        if '/formio/storage/filestore' in endpoint.routing.get('routes', []):
            auth_method = endpoint.routing["auth"]
            log = {
                'routes': endpoint.routing.get('routes'),
                'auth_method': auth_method,
                'request_user_id': request.env.user.id
            }
            _logger.debug(log)

            if auth_method == 'user' and request.env.user:
                auth_method = super(IrHttp, cls)._authenticate(endpoint)
                return auth_method
            else:
                _logger.debug('Allow public /formio/storage/filestore , become: auth=public')
                return 'public'
        else:
            return super(IrHttp, cls)._authenticate(endpoint)
