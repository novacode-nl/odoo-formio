# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models

import logging
_logger = logging.getLogger(__name__)


class FormComponent(models.Model):
    _name = 'formio.component'
    _rec_name = 'path_label'
    _description = 'Form Component'
    _order = 'builder_name asc, builder_version asc, sequence asc'

    builder_id = fields.Many2one(
        'formio.builder',
        string='Form Builder',
        required=True,
        ondelete='cascade'
    )
    builder_name = fields.Char(
        related='builder_id.name',
        string='Form Builder Name',
        store=True
    )
    builder_title = fields.Char(
        related='builder_id.title',
        string='Form Builder Title',
        store=True
    )
    builder_version = fields.Integer(
        related='builder_id.version',
        string='Form Builder Version',
        store=True
    )
    sequence = fields.Integer(string='Sequence')
    label = fields.Char(string='Label', required=True)
    key = fields.Char(string='Key', required=True)
    path_key = fields.Char(string='Path Keys', required=True, index=True)
    path_label = fields.Char(string='Path Labels', required=True, index=True)
    input_path_key = fields.Char(string='Input Path Keys', index=True)
    input_path_label = fields.Char(string='Input Path Labels', index=True)
    type = fields.Char(string='Type', required=True)
    input = fields.Boolean(string='Input')
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

    def builder_path_key_list2str(self, path_key_list):
        return '.'.join(path_key_list)
