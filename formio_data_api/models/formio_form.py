# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from formiodata.builder import Builder
from formiodata.form import Form

from odoo import models
from odoo.exceptions import UserError


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
                builder_obj = Builder(self.builder_id.schema, language=res_lang.iso_code, i18n=self.i18n_translations())

                if self.submission_data is False:
                    # HACK masquerade empty Form object
                    self._formio = Form('{}', builder_obj)
                else:
                    self._formio = Form(self.submission_data, builder_obj)
                return self._formio
        else:
            return self.__getattribute__(name)
