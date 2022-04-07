# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class Form(models.Model):
    _name = 'formio.mail.recipient.address'
    _description = 'Form Mail Recipient Mail Address'

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    name = fields.Char(
        string='Recipient Name'
    )
    email = fields.Char(
        string='Mail Address'
    )
