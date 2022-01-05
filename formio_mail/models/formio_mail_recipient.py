# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class Form(models.Model):
    _name = 'formio.mail.recipient'
    _description = 'Form Mail Recipient'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    name = fields.Char(
        string='Recipient Name'
    )
    email = fields.Char(
        string='Mail Address'
    )
    builder_ids = fields.Many2many(
        comodel_name='formio.builder',
        inverse_name='mail_recipients_ids',
        string='Form Builder'
    )
