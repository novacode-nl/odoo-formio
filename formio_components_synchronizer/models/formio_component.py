# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class FormioComponent(models.Model):
    _name = 'formio.component'
    _rec_name = 'label'
    _description = 'Formio Component'

    label = fields.Char(
        string='Label'
    )
    component_id = fields.Char(
        string='Component ID'
    )
    key = fields.Char(
        string='Key'
    )
    type = fields.Char(
        string='Type'
    )
    parent_id = fields.Many2one(
        'formio.component',
        string='Parent Component',
        index=True
    )
    child_ids = fields.One2many(
        'formio.component',
        'parent_id',
        string='Child Components'
    )
    builder_id = fields.Many2one(
        'formio.builder',
        string='Form Builder',
        required=True,
        ondelete='cascade'
    )

    @api.depends('label', 'key', 'parent_id')
    def name_get(self):
        res = []
        for r in self:
            if r.parent_id:
                label = '{parent}.{key} ({label})'.format(
                    parent=r.parent_id.key, key=r.key, label=r.label
                )
            else:
                label = '{key} ({label})'.format(
                    key=r.key, label=r.label
                )
            res.append((r.id, label))
        return res
