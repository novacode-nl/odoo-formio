# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from odoo import fields, models, api, tools, _

_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    # ----------------------------------------------------------
    # Model
    # ----------------------------------------------------------

    def write(self, vals):
        res = super(FormioBuilder, self).write(vals)
        if vals.get('schema'):
            self.synchronize_formio_components()
        return res

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    @api.model
    def _get_component(self, comp_id):
        """
        Returns a formio.component obj from component_id.
        """
        return self.env['formio.component'].search([
            ("builder_id", 'in', self.ids),
            ("component_id", '=', comp_id)
        ])

    @api.model
    def _compare_components(self):
        """
        Compares arrays with component keys.
        """
        new_components = []
        old_components = []
        for comp_id, obj in self._formio.component_ids.items():
            new_components.append(comp_id)
        for record in self.env['formio.component'].search([("builder_id", 'in', self.ids)]):
            old_components.append(record.component_id)
        return {
            'added': list(set(new_components).difference(old_components)),
            'deleted': list(set(old_components).difference(new_components))
        }

    @api.model
    def _write_components(self, comp_ids):
        """
        Writes the components with all required data to formio.component model.
        """
        for comp_id in comp_ids:
            obj = self._formio.component_ids[comp_id]
            self.env['formio.component'].create({
                'label': obj.label,
                'component_id': obj.id,
                'key': obj.key,
                'type': obj.type,
                'builder_id': self.id,
            })

    @api.model
    def _update_components(self):
        """
        Checks for any component related changes and synchronize them with database records.
        """
        for comp_id, obj in self._formio.component_ids.items():
            record = self._get_component(comp_id)
            if not record or record.component_id != obj.id:
                continue

            """
            Updating component attributes
            """
            if record.label != obj.label:
                record.label = obj.label
            if record.key != obj.key:
                record.key = obj.key

            """
            Updating datagrid
            """
            if obj.parent:
                if record.parent_id.component_id != obj.parent.id:
                    parent_record = self._get_component(obj.parent.id)
                    record.parent_id = parent_record
            elif not obj.parent and record.parent_id:
                record.parent_id = False

    @api.model
    def _delete_components(self, comp_ids):
        """
        Removes components from formio.component model.
        """
        for comp_id in comp_ids:
            components = self._get_component(comp_id)
            components.unlink()

    # ----------------------------------------------------------
    # Public
    # ----------------------------------------------------------

    @api.model
    def synchronize_formio_components(self):
        """
        Synchronize builder components with the formio.component model.
        """
        components_dict = self._compare_components()
        if components_dict['added']:
            self._write_components(components_dict['added'])
        if components_dict['deleted']:
            self._delete_components(components_dict['deleted'])
        self._update_components()
