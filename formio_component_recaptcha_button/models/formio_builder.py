# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class Builder(models.Model):
    _inherit = 'formio.builder'

    component_recaptcha_button_site_key = fields.Char(string='(odoo) reCAPTCHA Site Key', compute='_compute_recaptcha_button')
    component_recaptcha_button_active = fields.Boolean(string='(odoo) reCAPTCHA Active')

    def _compute_recaptcha_button(self):
        Config = self.env['ir.config_parameter'].sudo()
        site_key = Config.get_param('recaptcha_public_key')
        self.component_recaptcha_button_site_key = site_key
