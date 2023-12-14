# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from markupsafe import Markup

from formiodata.builder import Builder
from formiodata.form import Form

from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

UNKNOWN_ODOO_FIELD = 'UNKNOWN Odoo field'


class FormioForm(models.Model):
    _inherit = 'formio.form'

    def formio_component_class_mapping(self):
        """
        This method provides the formiodata.Builder instantiation the
        component_class_mapping keyword argument.

        This method can be implemented in other (formio) modules.
        """
        return {}

    def markupsafe(self, content, extra_replacements=[]):
        """ Escape characters so it is safe to use in HTML and XML
        :param extra_replacements
        """
        replacements = [['\n', '<br/>']]
        replacements += extra_replacements
        for rep in replacements:
            content = content.replace(rep[0], rep[1])
        return Markup(content)

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

                component_class_mapping = self.formio_component_class_mapping()
                res_lang = self.env['res.lang'].search([('code', '=', lang)], limit=1)
                builder_obj = Builder(
                    self.builder_id.schema,
                    language=res_lang.iso_code,
                    component_class_mapping=component_class_mapping,
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
