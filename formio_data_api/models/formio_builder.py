# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from formiodata.builder import Builder

from odoo import fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    component_server_api_ids = fields.One2many(
        'formio.component.server.api', 'formio_builder_id',
        string='Component Server APIs', context={'active_test': False})

    def _component_api_keys(self):
        return ['model_field', 'res_field', 'user_field', 'code_api']

    def action_current(self):
        self._validate_component_api_properties()
        super(FormioBuilder, self).action_current()
    
    def _validate_component_api_properties(self):
        builder = Builder(self.schema)

        for comp_name, component in builder.input_components.items():
            properties = component.properties or {}
            found_prefix_keys = {prefix: False for prefix in self._component_api_keys()}
            keys = self._component_api_keys()

            for prop_key, prop_val in properties.items():
                if any([prop_key == prefix for prefix in self._component_api_keys()]):
                    found_prefix_keys[prop_key] = True

            # TODO check all components and collect errors (log/raise only once)
            if sum([1 for check in found_prefix_keys.values() if check == True]) > 1:
                msg = _('Incorrect or conflicting "API Custom Properties" for Form Component, with:\n'
                        '- Label: %s\n'
                        '- Key: %s\n\n' \
                        'Custom Properties:\n' \
                        '%s')

                display_error = _(msg) % (component.label, component.key, properties)
                raise ValidationError(display_error)
