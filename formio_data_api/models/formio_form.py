# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from formiodata import builder, submission

from odoo import models
from odoo.exceptions import UserError


class Form(models.Model):
    _inherit = 'formio.form'

    def __getattr__(self, name):
        if name == '_formio':
            if 'formio' not in self.__dict__:
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

                builder_obj = builder.Builder(
                    self.builder_id.schema, res_lang.iso_code, context={'model_object': self})

                if self.submission_data is False:
                    # HACK masquerade empty Submission object on the formio attr.
                    self.formio = EmptySubmission(submisison_json, builder_obj)
                else:
                    self.formio = submission.Submission(self.submission_data, builder_obj)
            return self.formio
        else:
            return self.__getattribute__(name)
