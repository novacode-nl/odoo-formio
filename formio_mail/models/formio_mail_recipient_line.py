# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class Form(models.Model):
    _name = 'formio.mail.recipient.line'
    _description = 'Form Mail Recipient Line'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    builder_id = fields.Many2one(
        'formio.builder',
        string='Form Builder',
        required=True,
        ondelete='cascade'
    )
    mail_recipients_address_id = fields.Many2one(
        'formio.mail.recipient.address',
        string='Mail'
    )
    mail_recipients_formio_component_id = fields.Many2one(
        'formio.component',
        string='Component',
        domain="[('builder_id', '=', builder_id)]",
        help='List of formio components which should be used as source for mail recipients.'
    )
    mail_recipients_partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Use mail address from partner record.'
    )
    mail_report_id = fields.Many2one(
        'ir.actions.report',
        string="Report",
        domain=[('model', '=', 'formio.form')]
    )
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Template',
        domain=[('model', '=', 'formio.form')],
        ondelete='restrict',
        help='This field contains the template of the mail that will be automatically sent'
    )
