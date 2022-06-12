# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from odoo import fields, models, tools

_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    mail_active = fields.Boolean(
        string='Mailings active',
        help='Check this box to send submitted forms to recipients.'
    )

    mail_recipient_line = fields.One2many(
        'formio.mail.recipient.line',
        'builder_id',
        string='Mail Recipient Line'
    )

    def _get_recipients_from_component(self):
        """
        Computes all formio.components specified in the mail_recipients_formio_component_ids field.
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

    def _get_recipients_from_record(self, form):
        """
        Get's all mail recipients from res.partner and formio.mail.recipient.

        :return array: With mail recipients in a dictionary.
        """
        res = []
        for line in self.mail_recipient_line:
            for record in line.mail_recipients_partner_id:
                mail_values = {}
                mail = tools.email_split_and_format(record.email)
                if mail:
                    mail_values['recipient'] = mail[0]
                if record.lang:
                    mail_values['lang'] = record.lang
                mail_values['template'] = line.mail_template_id.id
                mail_values['report'] = line.mail_report_id.id
                res.append(mail_values)
            for record in line.mail_recipients_address_id:
                mail_values = {}
                mail = tools.email_split_and_format(record.email)
                if mail:
                    mail_values['recipient'] = mail[0]
                mail_values['template'] = line.mail_template_id.id
                mail_values['report'] = line.mail_report_id.id
                res.append(mail_values)
            for record in line.mail_recipients_formio_component_id:
                mail_values = {}
                component_values = []
                if record.key not in form._formio.input_components.keys():
                    continue
                obj = form._formio.input_components[record.key]
                component_values.extend(self._get_component_mail(obj))
                for value in component_values:
                    mail = tools.email_split_and_format(value)
                    if mail:
                        mail_values['recipient'] = mail[0]
                mail_values['template'] = line.mail_template_id.id
                mail_values['report'] = line.mail_report_id.id
                res.append(mail_values)
        return res

    def _get_component_mail(self, component):
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
                    res.extend(self._get_component_mail(inner_component))
            return res
        elif component.type == 'selectboxes':
            for key, value in component.value.items():
                if value:
                    res.append(key)
            return res
        elif component.type in ('email', 'select', 'textfield'):
            res.append(component.value)
            return res
        return res
