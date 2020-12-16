# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging
import re

from functools import reduce
from formiodata.builder import Builder
from formiodata.form import Form

from odoo import models
from odoo.exceptions import UserError

from odoo.addons.formio.models.formio_form import STATE_PENDING, STATE_DRAFT

_logger = logging.getLogger(__name__)

ODOO_PREFIX = 'Odoo'
ODOO_REFRESH_PREFIX = 'OdooRF'
ODOO_MODEL_PREFIX = 'OdooModel'

# IMPORTANT regarding the delimiter choice:
# - A dot "." results in undesired submission data, due to
# the Form.io Javascript library/API.
# - A dash is allowed, however causing issues with the ETL module (formio_etl).
ODOO_FIELD_DELIM = '__'

UNKNOWN_ODOO_FIELD = 'UNKNOWN Odoo field'


class FormioForm(models.Model):
    _inherit = 'formio.form'

    def __getattr__(self, name):
        if name == '_formio':
            if '_formio' not in self.__dict__:
                context = self._context
                if 'lang' in context:
                    lang = context['lang']
                elif 'lang' not in context and 'uid' in context:
                    lang = self.env['res.users'].browse(context['uid']).lang
                elif 'lang' not in context and 'uid' not in context:
                    lang = self.env['res.users'].browse(self.write_uid).lang
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
                    self._formio = Form('{}', builder_obj)
                else:
                    self._formio = Form(self.submission_data, builder_obj)
                return self._formio
        else:
            return self.__getattribute__(name)

    def _etl_odoo_data(self):
        data = super(FormioForm, self)._etl_odoo_data()

        if self.res_model_id:
            model_object = self.env[self.res_model_id.model].browse(self.res_id)
            for comp_name, comp in self._formio.builder.form_components.items():
                if comp_name == ODOO_MODEL_PREFIX:
                    data[comp_name] = self.res_model_id.model
                elif comp_name.startswith(ODOO_REFRESH_PREFIX) or (comp_name.startswith(ODOO_PREFIX) and self.state == STATE_PENDING):
                    val = self._etl_odoo_field_val(model_object, comp_name, comp)
                    data[comp_name] = val
        return data

    def _etl_odoo_field_val(self, res_model_object, formio_component_name, formio_component):
        fields = self._split_fields_token(formio_component_name)
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
                            one2many_fields = self._split_fields_token(comp['key'])
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
                    error_msg = "One2many field % expects a Form.io datagrid component %s" % model_object
                    error = EtlOdooFieldError(formio_component_name, field, msg)
                    _logger.info(error.message)
                    return error.odoo_field_val
            elif field_def.type == 'many2one':
                try:
                    model_object = getattr(model_object, field)
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

    def _split_fields_token(self, split_str):
        if split_str.startswith(ODOO_REFRESH_PREFIX):
            re_pattern = r'^%s\%s' % (ODOO_REFRESH_PREFIX, ODOO_FIELD_DELIM)
            res = re.sub(re_pattern, '', split_str).split(ODOO_FIELD_DELIM)
        elif split_str.startswith(ODOO_PREFIX):
            re_pattern = r'^%s\%s' % (ODOO_PREFIX, ODOO_FIELD_DELIM)
            res = re.sub(re_pattern, '', split_str).split(ODOO_FIELD_DELIM)
        else:
            res = split_str.split(ODOO_FIELD_DELIM)
        return res


class EtlOdooFieldError(Exception):
    def __init__(self, formio_component_name, field, msg):
        self.odoo_field_val = "ERROR: %s (%s)" % (field, msg)
        self.message = "[EtlOdooFieldError] %s: %s (%s)" % (formio_component_name, field, msg)
