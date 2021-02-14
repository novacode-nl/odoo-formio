# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class Form(models.Model):
    _inherit = 'formio.form'

    @api.multi
    def after_submit(self):
        super(Form, self).after_submit()
        if self.builder_id.mail_active:
            self.send_mail()

    @api.multi
    def send_mail(self):
        self.ensure_one()
        template = self.builder_id.mail_template_id
        recipients = self.builder_id.get_mail_recipients(self)
        attachment_ids = self.generate_attachment()
        context = self._context
        if 'lang' in context:
            lang = context['lang']
        elif 'lang' not in context and 'uid' in context:
            lang = self.env['res.users'].browse(context['uid']).lang
        elif 'lang' not in context and 'uid' not in context:
            lang = self.env['res.users'].browse(self.write_uid).lang
        else:
            raise UserError("The form can't be loaded. No (user) language was set.")

        for recipient in recipients:
            if 'lang' in recipient:
                lang = recipient['lang']
            template.with_context(lang=lang).send_mail(
                self.id,
                force_send=True,
                email_values={
                    'email_to': recipient,
                    'attachment_ids': [attachment.id for attachment in attachment_ids]
                }
            )

    @api.multi
    def generate_attachment(self):
        pdf = self.builder_id.mail_report_id.render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])

        attachment_name = '%s - %s' % (_('Form'), self.title)
        return self.env['ir.attachment'].create({
            'name': attachment_name,
            'type': 'binary',
            'datas': b64_pdf,
            'datas_fname': attachment_name + '.pdf',
            'store_fname': attachment_name,
            'res_model': self._name,
            'res_id': self.id,
        })

