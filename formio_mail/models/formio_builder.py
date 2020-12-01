# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from odoo import fields, models, api, tools, _

_logger = logging.getLogger(__name__)


class Builder(models.Model):
    _inherit = 'formio.builder'

    mail_active = fields.Boolean(string='Mailings active', help='Check this box to send submitted forms to recipients.')
    mail_recipients = fields.Char(string='Recipients', help='Comma-separated list of email addresses.')
    mail_recipients_form_components = fields.Char(string='Formio Component',
                                       help='Comma-separated list of formio components. '
                                            'Please, specify here the key of the component.')
    mail_recipients_partner_ids = fields.Many2many('res.partner', help='Use mail address from partner record.')
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

    """
    Get all recipients (comma separated) from the field mail_recipients.
    """
    def _get_mail_recipients(self):
        res = tools.email_split_and_format(self.mail_recipients)
        return res

    """
    Compute comma separated list of formio components and get the mail recipients from submitted form.
    """
    def _get_mail_recipients_form_components(self, form):
        mail_recipients_form_components = self.mail_recipients_form_components
        recipients = []
        if mail_recipients_form_components:
            components = mail_recipients_form_components.split(',')
            for c in components:
                component = c.split('->')
                if len(component) >= 2:
                    try:
                        outer_component = form._formio.components[component[0]]
                    except KeyError as e:
                        _logger.error("Exception: %s" % e)
                    inner_component = component[1]
                    recipients.extend(self._get_component(outer_component, inner_component))
                else:
                    try:
                        outer_component = form._formio.components[c]
                    except KeyError as e:
                        _logger.error("Exception: %s" % e)
                    recipients.extend(self._get_component(outer_component))
        res = []
        for r in recipients:
            res.extend(tools.email_split_and_format(r))
        return res

    """
    Get mail recipients from specified partners in the form.builder.
    """
    @api.multi
    def _get_mail_recipients_partner_ids(self):
        res = []
        for p in self.mail_recipients_partner_ids:
            res.extend(tools.email_split_and_format(p.email))
        return res

    """
    This function collects all mail recipients from form components, partner entries and mail_recipients field. 
    """
    def get_mail_recipients(self, form):
        res = []
        res.extend(self._get_mail_recipients())
        res.extend(self._get_mail_recipients_form_components(form))
        res.extend(self._get_mail_recipients_partner_ids())
        return res

    """
    Supported form.io components are:
     - datagrid
     - email
     - select
     - selectboxes
     - textfield
    """
    def _get_component(self, outer_component, inner_component=[]):
        res = []
        if outer_component.type == 'datagrid':
            for row in outer_component.rows:
                for obj in row:
                    inner_component = row[obj]['_object']
                    res.extend(self._get_component(inner_component))
            return res
        elif outer_component.type == 'email':
            res.append(self._get_value_simple(outer_component))
            return res
        elif outer_component.type == 'select':
            res.append(self._get_value_simple(outer_component))
            return res
        elif outer_component.type == 'selectboxes':
            res.extend(self._get_value_selectboxes(outer_component))
            return res
        elif outer_component.type == 'textfield':
            res.append(self._get_value_simple(outer_component))
            return res
        return res

    def _get_value_simple(self, component):
        return component.value

    def _get_value_selectboxes(self, component):
        res = []
        for key, value in component.value.items():
            if value:
                res.append(key)
        return res