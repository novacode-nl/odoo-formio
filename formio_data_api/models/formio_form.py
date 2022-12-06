# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from functools import reduce
from formiodata.builder import Builder
from formiodata.form import Form

from odoo import models
from odoo.exceptions import UserError
from odoo.tools import safe_eval

from odoo.addons.formio.models.formio_form import STATE_PENDING, STATE_DRAFT

_logger = logging.getLogger(__name__)

UNKNOWN_ODOO_FIELD = 'UNKNOWN Odoo field'


class FormioForm(models.Model):
    _inherit = 'formio.form'

    def __getattr__(self, name):
        if name == '_formio':
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
                    raise UserError("The form can't be loaded. No (user) language was set.")

                res_lang = self.env['res.lang'].search([('code', '=', lang)], limit=1)
                builder_obj = Builder(
                    self.builder_id.schema,
                    language=res_lang.iso_code,
                    i18n=self.builder_id.i18n_translations())

                if self.submission_data is False:
                    # HACK masquerade empty Form object
                    # TODO implement caching on the model object
                    # self._formio = Form('{}', builder_obj)
                    form = Form(
                        "{}",
                        builder_obj,
                        date_format=res_lang.date_format,
                        time_format=res_lang.time_format,
                    )
                else:
                    # TODO implement caching on the model object
                    # self._formio = Form(self.submission_data, builder_obj)
                    form = Form(
                        self.submission_data,
                        builder_obj,
                        date_format=res_lang.date_format,
                        time_format=res_lang.time_format,
                    )
                return form
        else:
            return self.__getattribute__(name)

    def _etl_odoo_data(self):
        """
        ETL (Odoo) data and prefill in the Form components which have been configured for this.
        To configure the Form Component follow the steps:
        - Edit component
        - Open the tab: API
        - Use and fill in the API *Custom Properties* as shown in the overview below.

        =====================
        API Custom Properties
        =====================

        1. user_field
        =============

        Loads the field value from the current/logged-in user object. Eg:
        - Create date
        - Field from the related partner_id, eg birthdate

        Example:

        Update the Formio Component (birthdate) value with the birthdate of the current user.

        ---------------------------------------------------------------------------------------
        | Key                              | Value                                            |
        ---------------------------------------------------------------------------------------
        | user_field                       | partner_id.birthdate                             |

        2. res_field
        ============

        Loads the field value from the Resource Model object. Eg:
        - name of a sale order
        - customer info (field) of the sale order

        noupdate (rules)
        ----------------
        Rules which determine whether the Formio Component value may be updated by the current res_field (value).

        res_field_noupdate (domain filter)
        ----------------------------------
        Domain filter on the Resource Model object.
        If the domain applies, the Formio Component value may NOT be updated with the res_field (value).

        Example:

        The Resource Model is a stock.picking.
        Don't update the Formio Component (weight) value with the Delivery Order email of the Lead,
        if the Picking Type code is either EF or GH.

        ---------------------------------------------------------------------------------------
        | Key                              | Value                                            |
        ---------------------------------------------------------------------------------------
        | res_field                        | weight                                           |
        | res_field_noupdate               | [('picking_type_id.code', 'in', ['EF', 'GH'])]   |
        ---------------------------------------------------------------------------------------

        3. res_model_field
        ==================

        Loads the field value from the Resource Model (res_model_id) its [ir.model.model] object.
        Eg to show the model name or description.

        Example:

        ---------------------------------------------------------------------------------------
        | Key                              | Value                                            |
        ---------------------------------------------------------------------------------------
        | res_model_field                  | model                                            |
        ---------------------------------------------------------------------------------------

        4. noupdate rules
        =================

        Global noupdate rules with predenece above other noupdate rules, which cannot be bypassed.

        4.1 noupdate_user
        -----------------

        Global rule has predenece above other noupdate rules. It cannot be bypassed.

        Example:

        Don't update the Formio Component value if the current user (partner) has function 'sales'
        (aka salespersion).

        ---------------------------------------------------------------------------------------
        | Key                              | Value                                            |
        ---------------------------------------------------------------------------------------
        | noupdate_user                    | [('partner_id.function_id.name', '=', 'sales')]  |
        ---------------------------------------------------------------------------------------

        4.2 noupdate_form
        -----------------

        Domain filter on the [formio.form] object.
        If the domain applies, the Formio Component value may NOT be updated with the res_field (value).

        Example:

        Don't update the Formio Component value if the Form state is Draft.

        ---------------------------------------------------------------------------------------
        | Key                              | Value                                            |
        ---------------------------------------------------------------------------------------
        | noupdate_form                    | [('state', '=', 'DRAFT')]                       |
        ---------------------------------------------------------------------------------------
        """

        # TODO exception handling, if safe_eval(domain_str) or merge lists fail ?
        data = super(FormioForm, self)._etl_odoo_data()

        # IMPORTANT:
        # Don't ETL (update) a form if it's state ain't Pending or Draft.
        # This makes no sense, because updated value can not be submitted (stored) in a completed form anyway.
        if self.state not in [STATE_PENDING, STATE_DRAFT]:
            return data

        # TODO-1: refactor both for (lopps) to separate functions
        for comp_key, comp in self._formio.input_components.items():
            value = False
            properties = comp.properties or {}

            # API: noupdate check on formio.form (domain)
            noupdate_form_domain = properties.get('noupdate_form')
            if noupdate_form_domain and self.filtered_domain(safe_eval.safe_eval(noupdate_form_domain)):
                continue

            # API: noupdate check on current user (domain)
            noupdate_user_domain = properties.get('noupdate_user')
            if noupdate_user_domain and self.env.user.filtered_domain(safe_eval.safe_eval(noupdate_user_domain)):
                continue

            if self.res_model_id and self.id:
                res_model_object = self.env[self.res_model_id.model].browse(self.res_id)
            else:
                res_model_object = False

            for prop_key, prop_val in properties.items():
                # API: resource model field value
                if self.res_model_id:
                    if prop_key == 'res_model_field':
                        # API: ir.model.model (object) field value
                        value = self._etl_odoo_field_val(self.res_model_id, comp)
                    elif prop_key == 'res_field' and res_model_object:
                        value = self._etl_res_field_value(res_model_object, comp)
                # API: current user field value
                if prop_key == 'user_field':
                    from_object = self.env.user
                    fields = prop_val.split('.')
                    while len(fields) > 0:
                        # traverse relational field eg Many2one: partner_id.back_account_id.name
                        if len(fields) > 1:
                            # from_object becomes the relational (Many2one) object
                            value = getattr(from_object, fields[0])
                            from_object = value
                            field = fields.pop(0)
                        else:
                            field = fields.pop(0)
                            value = getattr(from_object, field)
            if value:
                data[comp_key] = value

        # ETL components by model formio.component.value.code.api
        data.update(self._etl_component_server_api())

        return data

    def _etl_component_server_api(self):
        data = {}
        api_values = {}
        if self.builder_id.component_server_api_ids.filtered('active'):
            for comp_key, comp in self._formio.input_components.items():
                prop_api = comp.properties.get('server_api')
                prop_value = comp.properties.get('server_api_value')
                prop_value_obj = comp.properties.get('server_api_value_obj')
                if comp_key not in data and prop_api and prop_value:
                    component_server_api = self.builder_id.component_server_api_ids.filtered(lambda x: x.active and x.name == prop_api)
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
                        eval_context = self.builder_id._get_formio_eval_context(component_server_api, self, comp)
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

    def _etl_res_field_value(self, model_object, formio_component):
        """
        :param model_object object: Model object
        :param formio_component object: formiodata Component object
        """
        # TODO exception handling, if safe_eval(domain_str) or merge lists fail ?
        value = None
        properties = formio_component.properties or {}
        res_field_value = properties.get('res_field')
        noupdate_form_domain = properties.get('noupdate_form')
        res_field_noupdate_domain = properties.get('res_field_noupdate')
        update = True

        # first check formio.form whether to update
        if noupdate_form_domain:
            update = not self.filtered_domain(safe_eval.safe_eval(noupdate_form_domain))

        # if still may update, then check the resource model object
        if update:
            if res_field_noupdate_domain:
                update = not model_object.filtered_domain(safe_eval.safe_eval(res_field_noupdate_domain))

            if update:
                value = self._etl_odoo_field_val(model_object, res_field_value, formio_component)
        return value

    def _etl_odoo_field_val(self, model_object, field_getter, formio_component):
        """
        :param res_model_object object: Model object
        :param field_getter str: A string in Python getattr format eg 'partner_id.bank_id.name'
        :param formio_component object: A formio-data Component object
        """

        fields = field_getter.split('.')
        fields_done = []

        for field in fields:
            try:
                field_def = model_object._fields[field]
            except:
                error_msg = "field not found in model"
                error = EtlOdooFieldError(field_getter, field, error_msg)
                _logger.info(error.message)
                return error.odoo_field_val

            if field_def.type == 'one2many':
                # TODO many2many works here as well?
                if formio_component.type == 'datagrid':
                    one2many_records = getattr(model_object, field)
                    datagrid_rows = []
                    for record in one2many_records:
                        row = {}

                        for key, comp in formio_component.components.items():
                            if comp.properties.get('res_field'):
                                try:
                                    row[comp.key] = self._etl_res_field_value(record, comp)
                                except Exception as e:
                                    _logger.info('_etl_odoo_field_val: %s' % e)
                                    pass
                        datagrid_rows.append(row)
                    odoo_field_val = datagrid_rows
                else:
                    error_msg = "One2many field % expects a formio.js datagrid component %s" % model_object
                    error = EtlOdooFieldError(formio_component.name, field, error_msg)
                    _logger.info(error.message)
                    return error.odoo_field_val
            elif field_def.type == 'many2one':
                try:
                    model_object = getattr(model_object, field)
                    if not model_object:
                        return False
                    fields_done.append(field)
                except:
                    error_msg = "field not found in model"
                    error = EtlOdooFieldError(formio_component.name, field, error_msg)
                    _logger.info(error.message)
                    return error.odoo_field_val
            else:
                try:
                    odoo_field_val = getattr(model_object, field)
                    fields_done.append(field)
                except:
                    msg = "3. field not found"
                    error = EtlOdooFieldError(formio_component.name, field, msg)
                    _logger.info(error.message)
                    odoo_field_val = error.message
        return odoo_field_val


class EtlOdooFieldError(Exception):
    def __init__(self, formio_component_name, field, msg):
        self.odoo_field_val = "ERROR: %s (%s)" % (field, msg)
        self.message = "[EtlOdooFieldError] %s: %s (%s)" % (formio_component_name, field, msg)
