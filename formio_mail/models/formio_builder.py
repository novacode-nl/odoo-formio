# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from odoo import fields, models, api, tools, _

_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    mail_active = fields.Boolean(
        string='Mailings active',
        help='Check this box to send submitted forms to recipients.'
    )
    mail_recipients_ids = fields.Many2many(
        'formio.mail.recipient',
        string='Recipients'
    )
    mail_recipients_formio_component_ids = fields.Many2many(
        'formio.component',
        string='Formio Component',
        domain="[('builder_id', '=', id)]",
        help='List of formio components which should be used as source for mail recipients.'
    )
    mail_recipients_partner_ids = fields.Many2many(
        'res.partner',
        help='Use mail address from partner record.'
    )
    mail_report_id = fields.Many2one(
        'ir.actions.report',
        string="Report",
        domain=[('model', '=', 'formio.form')]
    )
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Mail Template',
        domain=[('model', '=', 'formio.form')],
        ondelete='restrict',
        help='This field contains the template of the mail that will be automatically sent'
    )

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    def _get_recipients_from_record(self):
        """
        Get's all mail recipients from res.partner and formio.mail.recipient.

        :return array: With mail recipients in a dictionary.
        """
        res = []
        for record in self.mail_recipients_partner_ids:
            mail = tools.email_split_and_format(record.email)
            mail_values = {}
            if mail:
                mail_values['recipient'] = mail[0]
            if record.lang:
                mail_values['lang'] = record.lang
            res.append(mail_values)
        for record in self.mail_recipients_ids:
            mail = tools.email_split_and_format(record.email)
            mail_values = {}
            if mail:
                mail_values['recipient'] = mail[0]
            res.append(mail_values)
        return res

    def _get_recipients_from_component(self, form):
        """
        Computes all formio.components specified in the mail_recipients_formio_component_ids field.

        :param record formio.form: Form record to get the component values from.
        :return array: With mail recipients in a dictionary.
        """
        values = []
        result = []
        components = self.mail_recipients_formio_component_ids
        for comp in components:
            if comp.key not in form._formio.input_components.keys():
                continue
            comp_obj = form._formio.input_components[comp.key]
            values.extend(self._get_component(comp_obj))
        for v in values:
            mail = tools.email_split_and_format(v)
            if mail:
                result.append({'recipient': mail[0]})
        return result

    # ----------------------------------------------------------
    # Formio Specific Helper Functions
    # ----------------------------------------------------------

    def _get_component(self, component):
        """
        Get's the value from a supported formio.component.
        Supported components are:
             - datagrid
             - email
             - select
             - selectboxes
             - textfield

        :param obj component: Takes a formio component object.
        :return array: With the value of the desired component.
        """
        res = []
        if component.type == 'datagrid':
            for row in component.rows:
                for obj in row:
                    inner_component = row[obj]['_object']
                    res.extend(self._get_component(inner_component))
            return res
        elif component.type == 'selectboxes':
            for key, value in component.value.items():
                if value:
                    res.append(key)
            return res
        elif component.type is 'email' or 'select' or 'textfield':
            res.append(component.value)
            return res
        return res

    # ----------------------------------------------------------
    # Public
    # ----------------------------------------------------------

    def get_mail_recipients(self, form):
        """
        This function collects all mail recipients from form components
        and database records.

        :param record form: the form record for getting mail recipients.
        :return array: With mail addresses of recipient.
        """
        res = []
        res.extend(self._get_recipients_from_record())
        res.extend(self._get_recipients_from_component(form))
        return res
