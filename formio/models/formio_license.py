# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from odoo import api, fields, models


class FormioLicense(models.Model):
    _name = 'formio.license'
    _description = 'Forms License'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    key = fields.Text('Key', required=True, tracking=True)
    valid_until_date = fields.Date(
        string='Valid Until',
        compute='_compute_license_fields',
        store=True
    )
    domains = fields.Char(
        string='Domains',
        compute='_compute_license_fields',
        store=True
    )
    active = fields.Boolean(string='Active', default=True, tracking=True)

    @api.depends('key')
    def _compute_license_fields(self):
        for rec in self:
            if rec.key:
                parts = self.key.split('#')
                part_dict = json.loads(parts[0])
                rec.valid_until_date = part_dict['validUntil']
                rec.domains = ', '.join(part_dict['domains'])

    def _compute_display_name(self):
        for rec in self:
            name = '%s %s' % (
                rec.domains, fields.Date.to_string(rec.valid_until_date)
            )
            rec.display_name = name
