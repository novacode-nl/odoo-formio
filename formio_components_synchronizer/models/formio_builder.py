# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging

from odoo import fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    component_sync_active = fields.Boolean(
        default=False,
        string='Synchronize Components',
        help='''By enabling "Synchronize Components" all components created/updated/deleted
        in the Form Builder will be automatically synchronized as formio.component records.'''
    )
    component_ids = fields.One2many(
        comodel_name="formio.component",
        inverse_name="builder_id",
        string="Components"
    )
    input_component_ids = fields.One2many(
        comodel_name="formio.component",
        inverse_name="builder_id",
        string="Input Components",
        domain=[('input', '=', True)]
    )

    def write(self, vals):
        res = super(FormioBuilder, self).write(vals)
        if 'schema' in vals and self.component_sync_active:
            self.synchronize_formio_components()
        return res

    def action_view_components(self):
        tree_view = self.env.ref(
            "formio_components_synchronizer.view_formio_builder_component_tree"
        )
        search_view = self.env.ref(
            "formio_components_synchronizer.view_formio_builder_component_search"
        )
        return {
            "name": _("Components"),
            "type": "ir.actions.act_window",
            "res_model": "formio.component",
            "domain": [("builder_id", "=", self.id)],
            "views": [
                [tree_view.id, "tree"],
                [False, "form"],
                [search_view.id, "search"],
            ],
        }

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    def _get_component(self, component_path_key):
        """
        Returns a formio.component obj from path.
        """
        self.ensure_one()
        return self.env['formio.component'].search([
            ("builder_id", '=', self.id),
            ("path_key", '=', component_path_key)
        ], limit=1)

    def _get_components(self, components=[], recur_components={}):
        self.ensure_one()
        Component = self.env['formio.component']
        if bool(recur_components):
            # check not empty Dict recur_components
            for comp_key, obj in recur_components.items():
                path_key = Component.builder_path_key_list2str(obj.builder_path_key)
                components.append(path_key)
                if obj.components:
                    self._get_components(components, obj.components)
        else:
            for comp_key, obj in self._formio.components.items():
                path_key = Component.builder_path_key_list2str(obj.builder_path_key)
                components.append(path_key)
                if obj.components:
                    self._get_components(components, obj.components)
        return components

    def _compare_components(self):
        """
        Compares arrays with component keys.
        """
        self.ensure_one()
        components = []
        new_components = self._get_components(components)
        old_components = []
        for record in self.env['formio.component'].search([("builder_id", 'in', self.ids)]):
            old_components.append(record.path_key)
        added = [c for c in new_components if c not in old_components]
        deleted = [c for c in old_components if c not in new_components]
        res = {
            'added': added,
            'deleted': deleted
        }
        return res

    def _write_components(self, components_path_key):
        """
        Writes the components with all required data to formio.component model.
        """
        self.ensure_one()
        Component = self.env['formio.component']
        sequence = 0
        for path_key in components_path_key:
            sequence = sequence + 1
            try:
                comp_obj = self._formio.components_path_key[path_key]
            except KeyError:
                msg = _("No component found with (generated) path %s in the Form Builder.") % path_key
                raise ValidationError(msg)
            self.env['formio.component'].sudo().create({
                'builder_id': self.id,
                'sequence': sequence,
                'label': comp_obj.label,
                'key': comp_obj.key,
                'path_key': path_key,
                'input_path_key': Component.builder_path_key_list2str(
                    comp_obj.builder_input_path_key
                ),
                'path_label': ' // '.join(comp_obj.builder_path_label),
                'input_path_label': ' // '.join(comp_obj.builder_input_path_label),
                'type': comp_obj.type,
                'input': comp_obj.input and comp_obj.is_form_component,
                'hidden': comp_obj.hidden,
                'disabled': comp_obj.disabled,
                'table_view': comp_obj.tableView,
                'clear_on_hide': comp_obj.clearOnHide,
                'required': comp_obj.required,
                'validate': json.dumps(comp_obj.validate, indent=4),
                'properties': json.dumps(comp_obj.properties, indent=4),
                'conditional': comp_obj.conditional,
                'custom_conditional': json.dumps(comp_obj.customConditional, indent=4),
                'templates': json.dumps(comp_obj.templates, indent=4),
                'logic': json.dumps(comp_obj.logic, indent=4),
            })

    def _update_components(self):
        """
        Checks for any component related changes and synchronize them with database records.
        """
        self.ensure_one()
        Component = self.env['formio.component']
        sequence = 0
        for path_key in self._get_components():
            comp_obj = self._formio.components_path_key.get(path_key)
            if not comp_obj:
                continue
            # determine component record
            record = self._get_component(path_key)
            record_sudo = record.sudo()
            sequence = sequence + 1
            record_sudo.sequence = sequence
            if not record or record.path_key != path_key:
                continue
            # update the component
            record_sudo._update_component(comp_obj)
            # update component parent (by path or data grids)
            # TODO move into formio.component _update_component method (above) ?
            if comp_obj.parent:
                if comp_obj.parent.builder_path_key:
                    parent_path_key = Component.builder_path_key_list2str(
                        comp_obj.parent.builder_path_key
                    )
                else:
                    parent_path_key = None
                # setter
                if (
                    parent_path_key
                    and hasattr(comp_obj.parent, "id")
                    and record_sudo.parent_id.path_key != parent_path_key
                ):
                    parent_record = self._get_component(parent_path_key)
                    record_sudo.parent_id = parent_record
                elif comp_obj.__class__.__name__ == "gridRow":
                    path_key_str = Component.builder_path_key_list2str(
                        comp_obj.grid.builder_path_key
                    )
                    parent_record = self._get_component(path_key_str)
                    record_sudo.parent_id = parent_record
                elif comp_obj.component_owner.__class__.__name__ == "gridRow":
                    path_key_str = Component.builder_path_key_list2str(
                        comp_obj.component_owner.grid.builder_path_key
                    )
                    parent_record = self._get_component(path_key_str)
                    record_sudo.parent_id = parent_record
                elif comp_obj.parent.__class__.__name__ == "gridRow":
                    path_key_str = Component.builder_path_key_list2str(
                        comp_obj.component_owner.builder_path_key
                    )
                    parent_record = self._get_component(path_key_str)
                    record_sudo.parent_id = parent_record
            elif not comp_obj.parent and record_sudo.parent_id:
                record_sudo.parent_id = False

    def _delete_components(self, components_path_key):
        """
        Delete components from formio.component model.
        """
        self.ensure_one()
        for path_key in components_path_key:
            component = self._get_component(path_key)
            component.unlink()

    # ----------------------------------------------------------
    # Public
    # ----------------------------------------------------------

    def synchronize_formio_components(self):
        """
        Synchronize builder components with the formio.component model.
        """
        self.ensure_one()
        components_dict = self._compare_components()
        if components_dict['added']:
            self._write_components(components_dict['added'])
        if components_dict['deleted']:
            self._delete_components(components_dict['deleted'])
        self._update_components()
