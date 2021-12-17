# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


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

    def unlink(self):
        if not self._context.get('formio_storage_filestore_force_unlink_attachment'):
            for attach in self:
                if attach.formio_storage_filestore_user_id and attach.res_model == 'formio.form' and attach.res_id:
                    msg = _("It's not allowed to delete an attachment which belongs to a Form (formio.form).") + \
                    '\n- ' + _('Attachment ID, name: %s, %s') % (attach.id, attach.name) + \
                    '\n- ' + _('Form (formio.form) ID: %s') % attach.res_id
                    raise UserError(msg)
        return super(IrAttachment, self).unlink()
