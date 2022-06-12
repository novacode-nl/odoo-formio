# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class MailRecipientLine(models.Model):
    _name = 'formio.mail.recipient.line'
    _description = 'Form Mail Recipient Line'

    builder_id = fields.Many2one(
        'formio.builder',
        string='Form Builder',
        ondelete='cascade'
    )
    builder_component_ids = fields.One2many(
        'formio.component',
        related='builder_id.component_ids',
    )

    ##################################################################
    # IMPORTANT:
    # The mail_recipients field values, could possibly store multiple
    # mail address (split by colon). Upon send mail, split by
    # tools.email_split_and_format
    ##################################################################

    mail_recipients_address_id = fields.Many2one(
        'formio.mail.recipient.address',
        string='Mail Recipient'
    )
    mail_recipients_formio_component_id = fields.Many2one(
        'formio.component',
        string='Component',
        domain="[('id', 'in', builder_component_ids)]",
        help='List of formio components which should be used as source for mail recipients.'
    )
    mail_recipients_formio_component_key = fields.Char(
        related='mail_recipients_formio_component_id.component_id',
        string='Component Key',
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
