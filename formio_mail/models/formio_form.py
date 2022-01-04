# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class Form(models.Model):
    _inherit = 'formio.form'

    def after_submit(self):
        super(Form, self).after_submit()
        if self.builder_id.mail_active:
            self.send_mail()

    def send_mail(self):
        self.ensure_one()
        template = self.builder_id.mail_template_id
        recipients = self.builder_id.get_mail_recipients(self)
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
