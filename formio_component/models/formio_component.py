# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from collections import defaultdict
from odoo import fields, models, api, _


class FormioComponent(models.Model):
    _name = 'formio.component'
    _rec_name = 'label'
    _description = 'Formio Component'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    label = fields.Char(
        string='Label'
    )
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        readonly=True,
        store=True
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
    parent_name = fields.Char(
        related='parent_id.display_name',
        string='Parent Component Name',
        readonly=True
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

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    def _compare_components(self, builder):
        """
        Compares arrays with component keys.

        :param tuple builder: the builder records to which the components belong,
        :return dict: with the deleted and added component_ids.

        {   'added': ['el1t2b', 'e2zvxh4', ...],
            'deleted': ['ejswb', 'ema9axd', ...]
        }

        """
        new_components = []
        old_components = []
        for comp_id, obj in builder._formio.component_ids.items():
            new_components.append(comp_id)
        for record in self.search([("builder_id", 'in', builder.ids)]):
            old_components.append(record.component_id)
        return {
            'added': list(set(new_components).difference(old_components)),
            'deleted': list(set(old_components).difference(new_components))
        }

    def _get_components(self, builder, comp_id):
        """
        Returns a formio.component obj from component_id.

        :param tuple builder: the builder records to which the component belongs,
        :param string comp_id: Component id of desired component in database,
        :return Database record according to builder_ids and comp_id.
        """
        return self.search([
            ("builder_id", 'in', builder.ids),
            ("component_id", '=', comp_id)
        ])

    @api.depends('label', 'parent_id')
    def _compute_display_name(self):
        """
        Computes the display name of formio.component.
        If it has parent it adds parents name to the display name.
        """
        for record in self:
            if record.parent_id:
                record.display_name = '%s.%s (%s)' % (record.parent_id.key, record.key, record.label)
            else:
                record.display_name = '%s (%s)' % (record.key, record.label)

    def _write_components(self, builder, comp_ids):
        """
        Writes the components with all required data to formio.component model.

        :param tuple builder: the builder where the components are located,
        :param array component_keys: components which should be added to this model.
        """
        for comp_id in comp_ids:
            obj = builder._formio.component_ids[comp_id]
            self.create({
                'label': obj.label,
                'component_id': obj.id,
                'key': obj.key,
                'type': obj.type,
                'builder_id': builder.id,
            })

    def _update_components(self, builder):
        """
        Checks for any component related changes and synchronize them with database records.

        :param builder: The builder where the components are located at.
        """
        for comp_id, obj in builder._formio.component_ids.items():
            record = self._get_components(builder, comp_id)
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
                    parent_record = self._get_components(builder, obj.parent.id)
                    record.parent_id = parent_record
            elif not obj.parent and record.parent_id:
                record.parent_id = False

    def _delete_components(self, builder, comp_ids):
        """
        Removes components from formio.component model.

        :param tuple builder: the builder record where the components are located,
        :param array component_keys: components which should be removed from this model.
        """
        for comp_id in comp_ids:
            components = self._get_components(builder, comp_id)
            components.unlink()

    # ----------------------------------------------------------
    # Public
    # ----------------------------------------------------------
    def synchronize_formio_components(self, builder_records=None):
        """
        Synchronize builder components with the formio.component model.

        :param tuple builder_records: builder records of components which should be synchronized
        and added or deleted to the formio.component model.
        """
        if builder_records is None:
            builder_records = self.env['formio.builder'].search([])
        for builder in builder_records:
            components_dict = self._compare_components(builder)
            if components_dict['added']:
                self._write_components(builder, components_dict['added'])
            if components_dict['deleted']:
                self._delete_components(builder, components_dict['deleted'])
            self._update_components(builder)
