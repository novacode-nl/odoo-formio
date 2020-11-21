# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, tools, _
import base64

STATE_COMPLETE = 'COMPLETE'


class Form(models.Model):
    _inherit = 'formio.form'

    @api.multi
    def action_submit(self):
        super(Form, self).action_submit()
        if self.builder_id.mail_active:
            self.action_send_mail()
        print(self.state)

    @api.multi
    def action_send_mail(self):
        self.ensure_one()
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)

        recipients = self.builder_id.get_mail_recipients(self)
        attachment_ids = self.generate_attachment()
        mails = self.env['mail.mail']
        for mail in recipients:
            mail_values = {
                'email_from': user.email,
                'reply_to': user.email,
                'email_to': mail,
                'subject': self.builder_id.mail_subject,
                'body_html': tools.html_sanitize(self.builder_id.mail_body_html, sanitize_attributes=True,
                                                 sanitize_style=True, strip_classes=True),
                'notification': True,
                'attachment_ids': [(4, attachment.id) for attachment in attachment_ids],
                'auto_delete': True,
            }
            mail = self.env['mail.mail'].create(mail_values)
            mails |= mail
        mails.send()
        return True

    @api.multi
    def generate_attachment(self):
        REPORT_ID = 'formio_report_qweb.action_report_formio_form'
        pdf = self.env.ref(REPORT_ID).render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])

        ATTACHMENT_NAME = 'Form.io Form -' + self.title
        return self.env['ir.attachment'].create({
            'name': ATTACHMENT_NAME,
            'type': 'binary',
            'datas': b64_pdf,
            'datas_fname': ATTACHMENT_NAME + '.pdf',
            'store_fname': ATTACHMENT_NAME,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })

