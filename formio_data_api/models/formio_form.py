# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging
import re

from functools import reduce
from formiodata.builder import Builder
from formiodata.form import Form

from odoo import models
from odoo.exceptions import UserError
from odoo.tools import safe_eval

from odoo.addons.formio.models.formio_form import STATE_PENDING, STATE_DRAFT, STATE_COMPLETE

_logger = logging.getLogger(__name__)

# DEPRECATION-1 remove these constants/vars
ODOO_PREFIX = 'Odoo'
ODOO_REFRESH_PREFIX = 'OdooRF'
ODOO_USER_PREFIX = 'OdooUser'
ODOO_MODEL_PREFIX = 'OdooModel'

# DEPRECATION-1 remove this constants/var
# IMPORTANT regarding the delimiter choice:
# - A dot "." results in undesired submission data, due to
# the formio.js Javascript library/API.
# - A dash is allowed, however causing issues with the ETL module (formio_etl).
ODOO_FIELD_DELIM = '__'

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

                # TODO remove unicode?
                schema_json = u'%s' % self.builder_id.schema
                builder_obj = Builder(
                    self.builder_id.schema,
                    language=res_lang.iso_code,
                    i18n=self.builder_id.i18n_translations())

                if self.submission_data is False:
                    # HACK masquerade empty Form object
                    # TODO implement caching on the model object
                    # self._formio = Form('{}', builder_obj)
                    form = Form('{}', builder_obj, date_format=res_lang.date_format, time_format=res_lang.time_format)
                else:
                    # TODO implement caching on the model object
                    # self._formio = Form(self.submission_data, builder_obj)
                    form = Form(self.submission_data, builder_obj, date_format=res_lang.date_format, time_format=res_lang.time_format)
                return form
        else:
            return self.__getattribute__(name)

    def _etl_odoo_data(self):
        """
        ETL (Odoo) data and prefill in the Form compoonents which have been configured for this.
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
        # Don't ETL (update) a form if it's state is Completed.
        # This makes no sense, because updated value can not be submitted (stored) in a completed form anyway.
        if self.state == STATE_COMPLETE:
            return data

        # TODO-1: refactor both for (lopps) to separate functions
        for comp_key, comp in self._formio.input_components.items():
            value = False
            properties = comp.properties or {}

            # DEPRECATION-1 cleanup with removal
            # If new ETL/API not determined, then run deprecated implementation.
            run_deprecated = True

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
                        run_deprecated = False
                        val = self._etl_odoo_field_val(self.res_model_id, comp)
                    elif prop_key == 'res_field' and res_model_object:
                        # API: resource model (object) field value
                        run_deprecated = False
                        value = self._etl_res_field_value(res_model_object, comp)
                # API: current user field value
                if prop_key == 'user_field':
                    run_deprecated = False

                    from_object = self.env.user
                    fields = prop_val.split('.')
                    while len(fields) > 0:
                        # traverse e.g: partner_id.back_account_id.name
                        field = fields.pop(0)
                        value = getattr(from_object, field)
                        if len(fields) > 1:
                            from_object = value

            # DEPRECATION-1 remove below
            if run_deprecated:
                value = self._deprecated_etl_odoo_data(comp)

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
                    api = self.builder_id.component_server_api_ids.filtered(lambda x: x.active and x.name == prop_api)
                    if not api:
                        _logger.error('NOT FOUND [formio.component.code.api] with name: %s' % prop_api)

                    if api and api_values.get(api.name):
                        value = api_values[api.name][prop_value]
                        if prop_value_obj:

                            # TODO-2: refactor DRY
                            value_fields = prop_value_obj.split('.')
                            value = reduce(getattr, value_fields, value)
                        data[comp_key] = value
                    elif api:
                        eval_context = self._get_formio_eval_context(comp)
                        # nocopy allows to return 'value'
                        safe_eval.safe_eval(api.code, eval_context, mode="exec", nocopy=True)
                        context_values = eval_context.get('value')
                        value = context_values.get(prop_value)
                        if prop_value_obj:
                            # TODO-2: refactor DRY
                            value_fields = prop_value_obj.split('.')
                            value = reduce(getattr, value_fields, value)
                        api_values[api.name] = context_values # caching
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
            update = not self.filtered_domain(safe_eval(noupdate_form_domain))

        # if still may update, then check the resource model object
        if update:
            if res_field_noupdate_domain:
                update = not model_object.filtered_domain(safe_eval(res_field_noupdate_domain))

            if update:
                value = self._etl_odoo_field_val(model_object, res_field_value, formio_component)
        return value

    # def _etl_odoo_field_val(self, res_model_object, formio_component_name, formio_component):
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
                    error = EtlOdooFieldError(formio_component_name, field, msg)
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
                    error = EtlOdooFieldError(formio_component_name, field, error_msg)
                    _logger.info(error.message)
                    return error.odoo_field_val
            else:
                try:
                    odoo_field_val = getattr(model_object, field)
                    fields_done.append(field)
                except:
                    msg = "3. field not found"
                    error = EtlOdooFieldError(formio_component_name, field, msg)
                    _logger.info(error.message)
                    odoo_field_val = error.message
        return odoo_field_val

    def _get_formio_eval_context(self, component):
        """ Prepare the context used when evaluating python code
            :returns: dict -- evaluation context given to safe_eval
        """
        return {
            'value': {},
            'env': self.env,
            'component': component,
            'record': self,
            'datetime': safe_eval.datetime,
            'dateutil': safe_eval.dateutil,
            'time': safe_eval.time,
        }

    ###############################################################
    # DEPRECATION-1
    # 
    # The functions below are deprecated and shall be removed soon.
    ###############################################################
    
    def _deprecated_etl_odoo_data(self, component):
        # DEPRECATION-1 remove

        val = False
        if component.key.startswith(ODOO_USER_PREFIX) and self.state in (STATE_PENDING, STATE_DRAFT):
            # Current user
            deprecation = """[DEPRECATION] OdooUser__ Component Property Name (key) is deprecated in favor of ...

            Use API Custom Properties (key): user_field, user_field_noupdate

            EXAMPLE:
            ----------------------------------------------------------------
            | Key                              | Value                     |
            ----------------------------------------------------------------
            | user_field                       | partner_id.birthdate      |
            ----------------------------------------------------------------

            More info: https://github.com/novacode-nl/odoo-formio/wiki/Prefill-Form-components-with-data-from-Odoo-(model-field)
            """
            _logger.warning(deprecation)
            val = self._deprecated_etl_odoo_field_val(self.env.user, component.key, component)
        elif self.res_model_id:
            # Form is linked with a resource object (eg crm.lead, sale.order etc)
            if component.key == ODOO_MODEL_PREFIX:
                # Resource model: ir.model (object)
                val = self._deprecated_etl_odoo_field_val(self.res_model_id, component.key, component)
            elif component.key.startswith(ODOO_REFRESH_PREFIX):
                deprecation = """[DEPRECATION] OdooRF__ Component Property Name (key) is deprecated in favor of ...

                Use API Custom Properties (key): res_field

                EXAMPLE:
                -----------------------------------------------------------------
                | Key                              | Value                      |
                ----------------------------------------------------------------
                | res_field                        | partner_shipping_id.street |
                -----------------------------------------------------------------

                More info: https://github.com/novacode-nl/odoo-formio/wiki/Prefill-Form-components-with-data-from-Odoo-(model-field)
                """
                _logger.warning(deprecation)

                # Resource model: always refresh/reload
                model_object = self.env[self.res_model_id.model].browse(self.res_id)
                val = self._deprecated_etl_odoo_field_val(model_object, component.key, component)
            elif component.key.startswith(ODOO_PREFIX) and self.state in (STATE_PENDING, STATE_DRAFT):
                # Resource model: only load if form state in [PENDING, DRAFT]
                # IMPORTANT: Keep this one last, because it's the always matching `Odoo` prefix.

                deprecation = """[DEPRECATION] Odoo__ Component (key) Property Name is deprecated in favor of ...

                Use API Custom Properties (keys): res_field, res_field_noupdate

                EXAMPLE 1 - noupdate if form matches domain (filter):
                -----------------------------------------------------------------
                | Key                              | Value                      |
                -----------------------------------------------------------------
                | res_field                        | partner_shipping_id.street |
                | nouppdate_form                   | [('state', '=', 'DRAFT')]  |
                ----------------------------------------------------------------

                EXAMPLE 2 - noupdate if res (resource object) matches domain (filter):
                -----------------------------------------------------------------
                | Key                              | Value                      |
                -----------------------------------------------------------------
                | res_field                        | partner_shipping_id.street |
                | nouppdate_res                    | [('field_x', '=', True)]   |
                -----------------------------------------------------------------

                More info: https://github.com/novacode-nl/odoo-formio/wiki/Prefill-Form-components-with-data-from-Odoo-(model-field)
                """
                _logger.warning(deprecation)
                model_object = self.env[self.res_model_id.model].browse(self.res_id)
                val = self._deprecated_etl_odoo_field_val(model_object, component.key, component)
        return val

    def _deprecated_etl_odoo_field_val(self, res_model_object, formio_component_name, formio_component):
        fields = self._deprecated_split_fields_token(formio_component_name)
        fields_done = []
        model_object = res_model_object

        for field in fields:
            try:
                field_def = model_object._fields[field]
            except:
                error_msg = "field not found in model"
                error = EtlOdooFieldError(formio_component_name, field, error_msg)
                _logger.info(error.message)
                return error.odoo_field_val

            if field_def.type == 'one2many':
                # TODO many2many works here as well?
                if formio_component.type == 'datagrid':
                    one2many_records = getattr(model_object, field)
                    datagrid_components = formio_component.raw.get('components')
                    datagrid_rows = []
                    for record in one2many_records:
                        row = {}
                        for comp in datagrid_components:
                            one2many_fields = self._deprecated_split_fields_token(comp['key'])
                            # XXX Exception handler checking one2many_fields exist, doesn't make sense here.
                            # Because additional/custom components can be present in datagrid row.
                            # For now just silence all exceptions here.
                            try:
                                row[comp['key']] = reduce(getattr, one2many_fields, record)
                                for one2many_field in one2many_fields:
                                    if one2many_field not in fields_done:
                                        fields_done.append(one2many_field)
                            except:
                                pass
                        datagrid_rows.append(row)
                    odoo_field_val = datagrid_rows
                else:
                    error_msg = "One2many field % expects a formio.js datagrid component %s" % model_object
                    error = EtlOdooFieldError(formio_component_name, field, msg)
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
                    error = EtlOdooFieldError(formio_component_name, field, error_msg)
                    _logger.info(error.message)
                    return error.odoo_field_val
            else:
                try:
                    odoo_field_val = getattr(model_object, field)
                    fields_done.append(field)
                except:
                    msg = "field not found"
                    error = EtlOdooFieldError(formio_component_name, field, msg)
                    _logger.info(error.message)
                    odoo_field_val = error.message
        return odoo_field_val

    def _deprecated_split_fields_token(self, split_str):
        # DEPRECATION-1 remove this function
        if split_str.startswith(ODOO_USER_PREFIX):
            re_pattern = r'^%s\%s' % (ODOO_USER_PREFIX, ODOO_FIELD_DELIM)
            res = re.sub(re_pattern, '', split_str).split(ODOO_FIELD_DELIM)
        elif split_str.startswith(ODOO_REFRESH_PREFIX):
            re_pattern = r'^%s\%s' % (ODOO_REFRESH_PREFIX, ODOO_FIELD_DELIM)
            res = re.sub(re_pattern, '', split_str).split(ODOO_FIELD_DELIM)
        elif split_str.startswith(ODOO_PREFIX):
            # IMPORTANT !
            # Keep this one last, because it's the always matching `Odoo` prefix.
            re_pattern = r'^%s\%s' % (ODOO_PREFIX, ODOO_FIELD_DELIM)
            res = re.sub(re_pattern, '', split_str).split(ODOO_FIELD_DELIM)
        else:
            res = split_str.split(ODOO_FIELD_DELIM)
        return res


class EtlOdooFieldError(Exception):
    def __init__(self, formio_component_name, field, msg):
        self.odoo_field_val = "ERROR: %s (%s)" % (field, msg)
        self.message = "[EtlOdooFieldError] %s: %s (%s)" % (formio_component_name, field, msg)
