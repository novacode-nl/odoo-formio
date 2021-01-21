# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models, api, _

COMPONENT_TYPES = [
            ('checkbox', 'Checkbox'),
            ('datagrid', 'Data Grid'),
            ('email', 'Email'),
            ('number', 'Number'),
            ('phoneNumber', 'Phone Number'),
            ('select', 'Select'),
            ('selectboxes', 'Select Boxes'),
            ('signature', 'Signature'),
            ('textarea', 'Text Area'),
            ('textfield', 'Text Field'),
        ]


class FormioComponent(models.Model):
    _name = 'formio.component'
    _description = 'Formio Component'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    name = fields.Char(
        string="Name"
    )

    display_name = fields.Char(
        string="Display Name",
        compute='_compute_display_name'
    )

    key = fields.Char(
        string="Unique Identifier"
    )

    type = fields.Selection(
        selection=COMPONENT_TYPES,
        string="Type"
    )

    parent_id = fields.Many2one(
        'formio.component',
        string='Parent Component'
    )

    child_ids = fields.One2many(
        'formio.component',
        'parent_id',
        string='Child Component'
    )

    builder_id = fields.Many2one(
        'formio.builder',
        string='Form Builder',
        required=True,
        ondelete='restrict'
    )

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    def _compare_components(self, old_components, new_components):
        """
        Compares arrays with component keys.

        :param array old_components: an array with the old component keys to compare,
        :param array new_components: an array with the components which are actually in the builder scheme to compare,
        :return dict: with the deleted and added keys.

        {   'added': ['textArea10', 'dataGrid', ...],
            'deleted': ['textField1', 'textArea3', ...]
        }

        """
        new_components = set(new_components)
        old_components = set(old_components)

        added = new_components.difference(old_components)
        deleted = old_components.difference(new_components)

        result = {
            'added': list(added),
            'deleted': list(deleted)
        }
        return result

    def _get_components(self, component_keys):
        """
        Returns multiple component_objs from component keys.

        :param array component_keys keys of components,
        :return tulp: with the component_ids.
        """
        return self.search([("key", '=', component_keys)])

    def _get_builder(self, builder_id):
        """
        Returns an builder_obj from builder_id.

        :param int builder_id the builder id which should be mapped to an builder_obj,
        :return tulp: with the builder_obj.
        """
        return self.env["formio.builder"].search([("id", '=', builder_id)])

    def _get_builder_component_keys(self, builder_id):
        """
        Fetch the components from specified builder and return it's component keys.

        :param int builder_id: the builder id where the components are located,
        :return array: with the component keys.
        """
        result = []
        builder_obj = self._get_builder(builder_id)
        for key, component in builder_obj._formio.components.keys():
            if component.raw.get('input') and component.type != 'button':
                if key in COMPONENT_TYPES:
                    result.append(key)
        return result

    def _get_model_components_keys(self, builder_id):
        """
        Fetch the components from the formio.component model filter by specified builder_ids.

        :param int builder_id: the builder id which should be used to search the model,
        :return array: with the component keys.
        """
        result = []
        records = self.search([("builder_id", '=', builder_id)])
        for record in records:
            result.append(record.key)
        return result

    def _compute_parents(self, builder_id):
        """
        Computes the parent and child dependency of an formio.component object.

        :param int builder_id: the id of the builder_id to compute,
        """
        builder_obj = self._get_builder(builder_id)
        component_obj = builder_obj.component_ids

        datagrid_obj = {}
        for obj in component_obj:
            if 'datagrid' in obj.type:
                datagrid_obj.append(obj)

        for datagrid in datagrid_obj:
            # TODO: Need to check if this function returns the desired value.
            components = datagrid._formio.items()
            for comp in components:
                component = self._get_components(comp)
                if component.id not in datagrid.child_ids:
                    datagrid.child_id += component.id
                if datagrid.id not in component.parent_id:
                    component.parent_id = datagrid.id

    def _compute_display_name(self):
        """
        Computes the display name of formio.component.
        If it has parent it adds parents name to the display name.
        """
        if self.parent_id:
            self.display_name = '%s.%s' % (self.parent_id.name, self.name)
        else:
            self.display_name = self.name

    def _write_components(self, components, builder_id):
        """
        Writes the components with all required data to formio.component model.

        :param array component_keys: components which should be added to this model.
        """
        compute_parents = False

        for component in components:
            self.create({
                'name': component['name'],
                'key': component['key'],
                'type': component['type'],
                'builder_id': builder_id,
            })
            if component.type == 'datagrid':
                compute_parents = True

        if compute_parents:
            self._compute_parents(builder_id)

    def _delete_components(self, component_keys):
        """
        Removes components from formio.component model.

        :param array component_keys: components which should be removed from this model.
        """
        components = self._get_components(component_keys)
        components.unlink()

    # ----------------------------------------------------------
    # Public
    # ----------------------------------------------------------

    def synchronize_components(self, builder_ids):
        """
        Synchronize builder components with the formio.component model.

        :param array builder_ids: builder ids of components which should be synchronized
        and added or deleted to the formio.component model.
        """
        for builder_id in builder_ids:
            new_components = self._get_builder_component_keys(builder_id)
            old_components = self._get_model_components_keys(builder_id)
            components_dict = self._compare_components(old_components, new_components)

            if components_dict['added']:
                self._write_components(components_dict['added'])
            if components_dict['deleted']:
                self._delete_components(components_dict['deleted'])
