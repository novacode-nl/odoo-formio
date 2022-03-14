# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, models


class Form(models.Model):
    _inherit = 'formio.form'

    @api.model
    def create(self, vals):
        res = super(Form, self).create(vals)
        if vals.get('submission_data'):
            res._process_storage_filestore_ir_attachments('create')
        return res

    def write(self, vals):
        res = super(Form, self).write(vals)
        for rec in self:
            if vals.get('submission_data'):
                rec._process_storage_filestore_ir_attachments('write')
        return res

    def unlink(self):
        """
        Workaround the ir.attachment its unlink implementation of this module.
        Which blocks deletion of attachment still linked to a user upload
        """
        domain = [
            ('res_model', '=', 'formio.form'),
            ('res_id', 'in', self.ids)
        ]
        attachments = self.env['ir.attachment'].search(domain)
        attachments.write({'formio_storage_filestore_user_id': False})
        return super(Form, self).unlink()

    def _process_storage_filestore_ir_attachments(self, mode):
        attach_names = []
        for key, component in self._formio.input_components.items():
            if component.type == 'datagrid':
                for row in component.rows:
                    for key, component_in_row in row.input_components.items():
                        attach_names += self._get_component_file_names(component_in_row)
            else:
                attach_names += self._get_component_file_names(component)

        # update ir.attachment (link with formio.form)
        if attach_names:
            domain = [
                ('name', 'in', attach_names),
                ('formio_storage_filestore_user_id', '!=', False)
            ]
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
                ('res_id', '=', self.id),
                ('formio_storage_filestore_user_id', '!=', False)
            ]
            if attach_names:
                domain.append(('name', 'not in', attach_names))
            self.env['ir.attachment'].search(domain).\
                with_context(formio_storage_filestore_force_unlink_attachment=True).\
                unlink()

    def _get_component_file_names(self, component_obj):
        names = []
        if hasattr(component_obj, 'storage') and component_obj.storage == 'url' \
           and '/formio/storage/filestore' in component_obj.url:
            for val in component_obj.value:
                names.append(val['name'])
        return names
