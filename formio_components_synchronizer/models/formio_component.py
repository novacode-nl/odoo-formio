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
    # component
    label = fields.Char(string='Label', required=True)
    key = fields.Char(string='Key', required=True)
    path_key = fields.Char(string='Path Keys', required=True, index=True)
    path_label = fields.Char(string='Path Labels', required=True, index=True)
    input_path_key = fields.Char(string='Input Path Keys', index=True)
    input_path_label = fields.Char(string='Input Path Labels', index=True)
    type = fields.Char(string='Type', required=True)
    input = fields.Boolean(string='Input')
    hidden = fields.Boolean(string='Hidden', default=True)
    disabled = fields.Boolean(string='Disabled', default=False)
    clear_on_hide = fields.Boolean(string='Clear Value When Hidden', default=True)
    table_view = fields.Boolean(string='Table View', default=True)
    required = fields.Boolean(string='Required', default=False)
    templates = fields.Text(string='Templates')
    logic = fields.Text(string='Logic')
    # TODO distinguish and implemnent custom validations
    validate = fields.Text(string='Validate')
    properties = fields.Text(string='API Properties')
    conditional = fields.Text(string='Conditional Simple')
    custom_conditional = fields.Text(string='Conditional Custom')

    def builder_path_key_list2str(self, path_key_list):
        return '.'.join(path_key_list)

    def _update_component(self, component):
        """
        Determine any change
        """
        self.ensure_one()
        Component = self.env['formio.component']
        vals = {}
        if self.label != component.label:
            vals['label'] = component.label
        if self.key != component.key:
            vals['key'] = component.key
        input_path_key = Component.builder_path_key_list2str(component.builder_input_path_key)
        if self.input_path_key != input_path_key:
            vals['input_path_key'] = input_path_key
        if self.hidden != component.hidden:
            vals['hidden'] = component.hidden
        if self.disabled != component.disabled:
            vals['disabled'] = component.disabled
        if self.table_view != component.tableView:
            vals['table_view'] = component.tableView
        if self.required != component.required:
            vals['required'] = component.required
        if self.clear_on_hide != component.clearOnHide:
            vals['clear_on_hide'] = component.clearOnHide
        if self.validate != component.validate:
            vals['validate'] = component.validate
        if self.properties != component.properties:
            vals['properties'] = component.properties
        if self.conditional != component.conditional:
            vals['conditional'] = component.conditional
        if self.custom_conditional != component.customConditional:
            vals['custom_conditional'] = component.customConditional
        if self.templates != component.templates:
            vals['templates'] = component.templates
        if self.logic != component.logic:
            vals['logic'] = component.logic
        # update
        if bool(vals):
            self.write(vals)
