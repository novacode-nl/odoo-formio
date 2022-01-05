# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from formiodata.builder import Builder
from odoo import fields, models, api, tools, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    # ----------------------------------------------------------
    # Model
    # ----------------------------------------------------------

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
                    raise UserError("The form can't be loaded. No (user) language was set.")

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

    def write(self, vals):
        res = super(FormioBuilder, self).write(vals)
        if vals.get('schema'):
            self.env['formio.component'].synchronize_formio_components(self)
        return res

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
            builder_records = self.search([])
        for builder in builder_records:
            components_dict = self.env['formio.component'].compare_components(builder)
            if components_dict['added']:
                self.env['formio.component'].write_components(builder, components_dict['added'])
            if components_dict['deleted']:
                self.env['formio.component'].delete_components(builder, components_dict['deleted'])
            self.env['formio.component'].update_components(builder)
