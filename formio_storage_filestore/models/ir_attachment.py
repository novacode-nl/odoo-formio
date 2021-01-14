# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class IrAttachment(models.AbstractModel):
    _inherit = 'ir.attachment'

    formio_storage_filestore_user_id = fields.Many2one('res.users')

    @api.model
    def cron_formio_storage_filestore_unlink_pending_attachments(self):
        domain = [
            ('formio_storage_filestore_user_id', '!=', False),
            ('res_model', '=', False),
            ('res_id', '=', False)
        ]
        self.search(domain).unlink()
