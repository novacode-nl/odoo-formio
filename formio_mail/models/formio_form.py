# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class Form(models.Model):
    _inherit = 'formio.form'

    def get_mail_recipients(self):
        """
        This function collects all mail recipients from form components
        and database records.
        """
        res = []
        res.extend(self.builder_id._get_recipients_from_record())
        res.extend(self._get_recipients_from_component())
        return res

    def _get_recipients_from_component(self):
        """
        Computes all formio.components specified in the mail_recipients_formio_component_ids field.
        :param record formio.form: Form record to get the component values from.
        :return array: With mail recipients in a dictionary.
        """
        values = []
        result = []
        components = self.builder_id.mail_recipients_formio_component_ids
        for comp in components:
            if comp.key not in self._formio.input_components.keys():
                continue
            comp_obj = self._formio.input_components[comp.key]
            values.extend(self.builder_id._get_component_mail(comp_obj))
        for v in values:
            mail = tools.email_split_and_format(v)
            if mail:
                result.append({'recipient': mail[0]})
        return result

    def after_submit(self):
        super(Form, self).after_submit()
        if self.builder_id.mail_active:
            self.send_mail()

    def send_mail(self):
        self.ensure_one()
        template = self.builder_id.mail_template_id
        recipients = self.get_mail_recipients()
        attachment_ids = self.generate_attachment()
        context = self._context

        if not template or not attachment_ids:
            return

        if 'lang' in context:
            lang = context['lang']
        elif 'lang' not in context and 'uid' in context:
            lang = self.env['res.users'].browse(context['uid']).lang
        elif 'lang' not in context and 'uid' not in context:
            lang = self.env['res.users'].browse(self.write_uid).lang
        else:
            raise UserError("The form can't be loaded. No (user) language was set.")

        for mail_values in recipients:
            if 'lang' in mail_values:
                lang = mail_values['lang']
            template.with_context(lang=lang).send_mail(
                self.id,
                force_send=True,
                email_values={
                    'email_to': mail_values['recipient'],
                    'attachment_ids': [attachment.id for attachment in attachment_ids]
                }
            )

    def generate_attachment(self):
        content, content_type = self.builder_id.mail_report_id._render(self.ids)
        attachment_name = '%s - %s' % (_('Form'), self.title)
        return self.env['ir.attachment'].create({
            'name': attachment_name,
            'type': 'binary',
            'datas': base64.encodebytes(content),
            'res_model': self._name,
            'res_id': self.id,
        })
