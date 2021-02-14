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

    mail_recipients = fields.Char(
        string='Recipients',
        help='Comma-separated list of email addresses.'
    )

    mail_formio_component_ids = fields.Many2many(
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
        required=True,
        ondelete='restrict',
        help='This field contains the template of the mail that will be automatically sent'
    )

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    def _get_recipients_from_field(self):
        """
        Get's all mail recipients from the mail_recipients field.
        Addresses specified in this field are comma-separated.

        :return array: With mail recipients in a dictionary.
        """
        res = []
        mail = tools.email_split_and_format(self.mail_recipients)
        if mail:
            res.append({
                'recipient': mail[0]
            })
        return res

    def _get_recipients_from_components(self, form):
        """
        Computes all formio.components specified in the mail_formio_component_ids field.

        :param record formio.form: Form record to get the component values from.
        :return array: With mail recipients in a dictionary.
        """
        formio_components = self.mail_formio_component_ids
        recipients = []
        for component in formio_components:
            component_obj = form._formio.components[component.key]
            recipients.extend(self._get_component(component_obj))
        res = []
        for r in recipients:
            mail = tools.email_split_and_format(r)
            if mail:
                res.append({
                    'recipient': mail[0]
                })
        return res

    @api.multi
    def _get_recipients_from_partner(self):
        """
        Computes all specified res.partner records in the mail_recipients_partner_ids field.

        :return array: With mail recipients and partner lang in a dictionary.
        """
        res = []
        for partner in self.mail_recipients_partner_ids:
            mail = tools.email_split_and_format(partner.email)
            mail_values = {}
            if mail:
                mail_values['recipient'] = mail[0]
            if partner.lang:
                mail_values['lang'] = partner.lang
            res.append(mail_values)
        return res

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

        :param obj component: Takes an component object.
        :return array: With the value of the desired component.
        """
        res = []
        if component.type == 'datagrid':
            for row in component.rows:
                for obj in row:
                    inner_component = row[obj]['_object']
                    res.extend(self._get_component(inner_component))
            return res
        elif component.type == 'email':
            res.append(self._get_value_simple(component))
            return res
        elif component.type == 'select':
            res.append(self._get_value_simple(component))
            return res
        elif component.type == 'selectboxes':
            res.extend(self._get_value_selectboxes(component))
            return res
        elif component.type == 'textfield':
            res.append(self._get_value_simple(component))
            return res
        return res

    def _get_value_simple(self, component):
        """
        Computes simple formio.components.

        :param component: Takes an component object.
        :return char: With the value of the desired component.
        """
        return component.value

    def _get_value_selectboxes(self, component):
        """
        Computes formio.components with the type of selectbox.

        :param component: Takes an selectbox component object.
        :return array: With the value of checked elements on the selectbox component.
        """
        res = []
        for key, value in component.value.items():
            if value:
                res.append(key)
        return res

    # ----------------------------------------------------------
    # Public
    # ----------------------------------------------------------

    def get_mail_recipients(self, form):
        """
        This function collects all mail recipients from form components,
        partner entries and mail_recipients field.

        :param record form: the form record for getting mail recipients.
        :return array: With mail addresses of recipient.
        """
        res = []
        res.extend(self._get_recipients_from_field())
        res.extend(self._get_recipients_from_components(form))
        res.extend(self._get_recipients_from_partner())
        return res
