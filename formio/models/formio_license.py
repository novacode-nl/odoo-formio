# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from odoo import api, fields, models
# from odoo.exceptions import ValidationError


class FormioLicense(models.Model):
    _name = 'formio.license'
    _description = 'Forms License'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    key = fields.Text('Key', required=True, tracking=True)
    valid_until_date = fields.Date(
        string='Valid Until',
        compute='_compute_license_fields',
        required=True,
        store=True
    )
    domains = fields.Char(
        string='Domains',
        compute='_compute_license_fields',
        required=True,
        store=True
    )
    active = fields.Boolean(string='Active', default=False, tracking=True)

    @api.depends('key')
    def _compute_license_fields(self):
        for rec in self:
            parts = self.key.split('#')
            part_dict = json.loads(parts[0])
            rec.valid_until_date = part_dict['validUntil']
            rec.domains = ', '.join(part_dict['domains'])

    # @api.constrains('active')
    # def _constraint_active(self):
    #     domain = [('active', '=', self.active)]
    #     if self.search_count(domain) > 1:
    #         raise ValidationError(_('Only 1 license can be active.'))
