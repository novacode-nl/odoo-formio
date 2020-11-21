# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import re

from odoo import fields, models, api, _


class Builder(models.Model):
    _inherit = 'formio.builder'

    mail_active = fields.Boolean(string='Mailings active', help='Check this box to send submitted forms to recipients.')
    mail_recipients = fields.Char(string='Recipients', help='Comma-separated list of email addresses.')
    mail_recipients_form = fields.Char(string='Formio Component',
                                       help='Comma-separated list of formio components. '
                                            'Please, specify here the key of the component.')
    mail_recipients_partner = fields.Many2many('res.partner', help='Use mail address from partner record.')
    mail_subject = fields.Char(default=lambda s: _('Test Subject'),
                               string='Subject')
    mail_body_html = fields.Html(default=lambda s: _('Dear Sirs and Mesdames, this needs to be replaced.'),
                                 string='Body',
                                 sanitize_attributes=False)

    def _get_mail_recipients(self):
        mail = self.mail_recipients.split(',')
        res = []
        for m in mail:
            if self.is_mail(m):
                res.append(m)
        return res

    def _get_mail_recipients_form(self, form):
        components = self.mail_recipients_form.split(',')
        res = []
        for c in components:
            if self.is_mail(c):
                res.append(form._formio.components[c].value)
        return res

    def _get_mail_recipients_partner(self):
        res = []
        for p in self.mail_recipients_partner:
            if self.is_mail(p.email):
                res.append(p.email)
        return res

    def get_mail_recipients(self, form):
        res = []
        res.extend(self._get_mail_recipients())
        res.extend(self._get_mail_recipients_form(form))
        res.extend(self._get_mail_recipients_partner())
        return res

    @api.onchange('email_id')
    def is_mail(self, mail):
        if mail:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', mail)
        if match is None:
            return False
        else:
            return True
