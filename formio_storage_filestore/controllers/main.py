# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64
import io
import json

from odoo import http
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class FormioStorageFilestoreController(http.Controller):
    """
    Although the type of authentication implies an authenticated user,
    requests for public (not authenticated) users will also be handled
    here. The override of the _authenticate method in the [ir.http]
    model handles this.
    """

    @http.route('/formio/storage/filestore', type='http', auth='user', methods=['POST'], csrf=False)
    def storage_filestore_post(self, **kwargs):
        """Process a (file) upload from the Form and create the
        corresponding `ir.attachment`.

        Distinguish auth=user and auth=public, implemented in the ir.http model.
        """
        IrAttachment = request.env['ir.attachment']

        # Avoid using sudo when not necessary: internal users can
        # create attachments, as opposed to public and portal users.
        if not request.env.user.has_group('base.group_user'):
            IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)

        uid = request._context.get('uid') or request.env.ref('base.public_user').id
        vals = {
            'name': kwargs.get('name'),
            'formio_storage_filestore_user_id': uid,
            'datas': base64.b64encode(kwargs.get('file').read()),
        }
        attachment = IrAttachment.create(vals)
        return request.make_response(
            data=json.dumps(attachment.read(['id', 'name', 'mimetype', 'file_size'])[0]),
            headers=[('Content-Type', 'application/json')]
        )

    @http.route('/formio/storage/filestore', type='http', auth='user', methods=['GET'])
    def storage_filestore_get(self, **kwargs):
        """Get a (file) upload from the Form by searching the
        corresponding `ir.attachment`.
        """
        IrAttachment = request.env['ir.attachment']

        # Avoid using sudo when not necessary: internal users can
        # create attachments, as opposed to public and portal users.
        if not request.env.user.has_group('base.group_user'):
            IrAttachment = IrAttachment.sudo().with_context(binary_field_real_user=IrAttachment.env.user)

        file_name = kwargs.get('form')
        if file_name.startswith('/'):
            file_name = file_name[1:]

        if file_name:
            domain = [
                ('name', '=', file_name),
                ('formio_storage_filestore_user_id', '!=', False)
            ]
            attachment = IrAttachment.search(domain)
            if not attachment:
                _logger.warning('ir.attachment not found for name: %s' % file_name)
                return request.not_found(file_name)
            elif len(attachment) > 1:
                _logger.warning('Found multiple ir.attachment for name %s' % file_name)
                return request.not_found(file_name)
            else:
                attachment = attachment[0]
                data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
                response = http.send_file(data, filename=attachment['name'], as_attachment=True)
                return response
