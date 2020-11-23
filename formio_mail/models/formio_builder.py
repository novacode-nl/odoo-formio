# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from odoo import fields, models, api, tools, _

_logger = logging.getLogger(__name__)


class Builder(models.Model):
    _inherit = 'formio.builder'

    mail_active = fields.Boolean(string='Mailings active', help='Check this box to send submitted forms to recipients.')
    mail_recipients = fields.Char(string='Recipients', help='Comma-separated list of email addresses.')
    mail_recipients_form = fields.Char(string='Formio Component',
                                       help='Comma-separated list of formio components. '
                                            'Please, specify here the key of the component.')
    mail_recipients_partner = fields.Many2many('res.partner', help='Use mail address from partner record.')
    mail_subject = fields.Char(default=lambda s: _('Form.Io - You\'ve received a Form'),
                               string='Subject')
    mail_body_html = fields.Html(default=lambda s: _('''Dear Recipient, <br/>
                                                        you've received a filled form. In the attachments, you'll find 
                                                        the report in pdf format. <br/>
                                                        Greetings <br/>
                                                        Your form system'''),
                                 string='Body',
                                 sanitize_attributes=False)
    mail_report_id = fields.Many2one('ir.actions.report', string="Report", domain=[('model', '=', 'formio.form')])

    def _get_mail_recipients(self):
        res = tools.email_split_and_format(self.mail_recipients)
        return res

    def _get_mail_recipients_form(self, form):
        mail_recipients_form = self.mail_recipients_form
        res = []
        if mail_recipients_form:
            components = mail_recipients_form.split(',')
            for c in components:
                try:
                    res.extend(tools.email_split_and_format(form._formio.components[c].value))
                except KeyError as e:
                    _logger.error("Exception: %s" % e)
        return res

    @api.multi
    def _get_mail_recipients_partner(self):
        res = []
        for p in self.mail_recipients_partner:
            res.extend(tools.email_split_and_format(p.email))
        return res

    def get_mail_recipients(self, form):
        res = []
        res.extend(self._get_mail_recipients())
        res.extend(self._get_mail_recipients_form(form))
        res.extend(self._get_mail_recipients_partner())
        return res
