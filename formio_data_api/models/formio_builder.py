# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from formiodata.builder import Builder

from odoo import models, _
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    def formio_component_class_mapping(self):
        """
        This method provides the formiodata.Builder instantiation the
        component_class_mapping keyword argument.

        This method can be implemented in other (formio) modules.
        """
        return {}

    def __getattr__(self, name):
        if name == '_formio' and self._name == 'formio.builder':
            # TODO implement caching on the model object
            # self._cache or self.env.cache API only works for model fields, not Python attr.

            # if '_formio' not in self.__dict__:
            no_cache = True
            if no_cache:
                context = self._context
                if 'lang' in context:
                    lang = context['lang']
                elif 'lang' not in context and 'uid' in context:
                    lang = self.env['res.users'].browse(context['uid']).lang
                elif 'lang' not in context and 'uid' not in context:
                    lang = self.write_uid.lang
                else:
                    raise UserError("The form builder can't be loaded. No (user) language was set.")

            if self.schema is False:
                # HACK masquerade empty Builder object
                builder_obj = Builder('{}')
            else:
                component_class_mapping = self.formio_component_class_mapping()
                builder_obj = Builder(
                    self.schema,
                    language=self.env['res.lang'].sudo()._formio_ietf_code(lang),
                    component_class_mapping=component_class_mapping,
                    i18n=self.i18n_translations()
                )
            return builder_obj
        else:
            return self.__getattribute__(name)

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
            for prop_key, prop_val in properties.items():
                if any([prop_key == prefix for prefix in self._component_api_keys()]):
                    found_prefix_keys[prop_key] = True
            # TODO check all components and collect errors (log/raise only once)
            if sum([1 for check in found_prefix_keys.values() if check]) > 1:
                msg = _('Incorrect or conflicting "API Custom Properties" for Form Component, with:\n'
                        '- Label: %s\n'
                        '- Key: %s\n\n'
                        'Custom Properties:\n'
                        '%s')

                display_error = _(msg) % (component.label, component.key, properties)
                raise ValidationError(display_error)
