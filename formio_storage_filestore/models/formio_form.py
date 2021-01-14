# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, models


class Form(models.Model):
    _inherit = 'formio.form'

    @api.model
    def create(self, vals):
        res = super(Form, self).create(vals)

        res._process_storage_filestore_ir_attachments('create')
        return res

    def write(self, vals):
        submission_data = self.submission_data
        res = super(Form, self).write(vals)
        self._process_storage_filestore_ir_attachments('write')
        return res

    def _process_storage_filestore_ir_attachments(self, mode):
        attach_names = []
        for key, component in self._formio.components.items():
            if hasattr(component, 'storage') and component.storage == 'url' \
               and '/formio/storage/filestore' in component.url:
                for val in component.value:
                    attach_names.append(val['name'])

        # update ir.attachment (link with formio.form)
        if attach_names:
            domain = [('name', 'in', attach_names)]
            attachments = self.env['ir.attachment'].search(domain)
            for attach in attachments:
                vals = {
                    'res_model': 'formio.form',
                    'res_id': self.id,
                }
                attach.write(vals)

        # delete ir.attachment (deleted files)
        if mode == 'write':
            domain = [
                ('res_model', '=', 'formio.form'),
                ('res_id', '=', self.id)
            ]
            if attach_names:
                domain.append(('name', 'not in', attach_names))
            self.env['ir.attachment'].search(domain).unlink()
