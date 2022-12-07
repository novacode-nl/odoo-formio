# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from functools import reduce
from formiodata.builder import Builder

from odoo import fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import safe_eval


_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    component_server_api_ids = fields.One2many(
        'formio.component.server.api', 'formio_builder_id',
        string='Component Server APIs', copy=True, context={'active_test': False})

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

                res_lang = self.env['res.lang'].search([('code', '=', lang)], limit=1)

            if self.schema is False:
                # HACK masquerade empty Builder object
                builder_obj = Builder('{}')
            else:
                builder_obj = Builder(
                    self.schema,
                    language=res_lang.iso_code,
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

    def _get_formio_eval_context(self, component_server_api, formio_form=None, component=None, params={}):
        """ Prepare the context used when evaluating python code

        :param component_server_api: formio.component.server.api model record object
        :param formio_form: formio.form model record object
        :param component: formiodata Component object
        :param params: possible dict with data, eg from URL query params
            by the /data URL endpoint
        :returns: dict -- evaluation context given to safe_eval
        """
        res = {
            'env': self.env,
            'builder': self,
            'record': formio_form,
            'form': formio_form,
            'datetime': safe_eval.datetime,
            'dateutil': safe_eval.dateutil,
            'time': safe_eval.time,
            'component': component,
            'params': params
        }
        if component_server_api.type == 'values':
            res['values'] = {}
        return res

    def _etl_odoo_data(self, params={}):
        """
        ETL (Odoo) data and prefill in the Form components.
        """
        res = super(FormioBuilder, self)._etl_odoo_data(params)
        res.update(self._etl_component_server_api(params=params))
        return res

    def _etl_component_server_api(self, params={}):
        data = {}
        api_values = {}
        if self.component_server_api_ids.filtered('active'):
            for comp_key, comp in self._formio.input_components.items():
                prop_api = comp.properties.get('server_api')
                prop_value = comp.properties.get('server_api_value')
                prop_value_obj = comp.properties.get('server_api_value_obj')

                if comp_key not in data and prop_api and prop_value:
                    component_server_api = self.component_server_api_ids.filtered(lambda x: x.active and x.name == prop_api)
                    if not component_server_api:
                        _logger.error('NOT FOUND [formio.component.code.api] with name: %s' % prop_api)

                    if component_server_api and api_values.get(component_server_api.name):
                        value = api_values[component_server_api.name][prop_value]
                        if prop_value_obj:
                            # TODO-2: refactor DRY
                            value_fields = prop_value_obj.split('.')
                            value = reduce(getattr, value_fields, value)
                        data[comp_key] = value
                    elif component_server_api:
                        eval_context = self._get_formio_eval_context(component_server_api, self, comp, params=params)
                        # nocopy allows to return 'value'
                        safe_eval.safe_eval(component_server_api.code, eval_context, mode="exec", nocopy=True)
                        context_values = eval_context.get('values')
                        value = context_values.get(prop_value)
                        if prop_value_obj:
                            # TODO-2: refactor DRY
                            value_fields = prop_value_obj.split('.')
                            value = reduce(getattr, value_fields, value)
                        # caching
                        if context_values:
                            api_values[component_server_api.name] = context_values
                        data[comp_key] = value
        return data
