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
        recipients = self.builder_id._get_recipients_from_record(self)
        attachments = self._prepare_attachment(recipients)
        context = self._context

        if 'lang' in context:
            lang = context['lang']
        elif 'lang' not in context and 'uid' in context:
            lang = self.env['res.users'].browse(context['uid']).lang
        elif 'lang' not in context and 'uid' not in context:
            lang = self.env['res.users'].browse(self.write_uid).lang
        else:
            raise UserError("The form can't be loaded. No (user) language was set.")

        for mail_values in recipients:
            report_id = mail_values['report']
            if not all(k in mail_values for k in ('template', 'report', 'recipient')):
                continue
            if 'lang' in mail_values:
                lang = mail_values['lang']
            if report_id in attachments:
                attachment_id = attachments[report_id]
                template = self.env['mail.template'].browse(mail_values['template'])
                attachment_ids = self.env['ir.attachment'].browse(attachment_id)

                if template and attachment_ids:
                    template.with_context(lang=lang).send_mail(
                        self.id,
                        force_send=True,
                        email_values={
                            'email_to': mail_values['recipient'],
                            'attachment_ids': [attachment.id for attachment in attachment_ids]
                        }
                    )

    def _prepare_attachment(self, recipients):
        reports = []
        result = {}
        for r in recipients:
            if r['report'] not in reports:
                reports.append(r['report'])
        for r in reports:
            report = self.env['ir.actions.report'].browse(r)
            attachment_ids = self.generate_attachment(report)
            result[r] = attachment_ids.id
        return result

    def generate_attachment(self, report):
        content, content_type = report._render(self.ids)
        attachment_name = '%s - %s.pdf' % (_('Form'), self.title)
        return self.env['ir.attachment'].create({
            'name': attachment_name,
            'type': 'binary',
            'datas': base64.encodebytes(content),
            'res_model': self._name,
            'res_id': self.id,
        })
