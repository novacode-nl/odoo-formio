# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from copy import copy

from odoo import fields, models


class Builder(models.Model):
    _inherit = 'formio.builder'

    component_recaptcha_button_site_key = fields.Char(string='(odoo) reCAPTCHA Site Key', compute='_compute_recaptcha_button')
    component_recaptcha_button_active = fields.Boolean(string='(odoo) reCAPTCHA Active')

    def _compute_recaptcha_button(self):
        Config = self.env['ir.config_parameter'].sudo()
        site_key = Config.get_param('recaptcha_public_key')
        self.component_recaptcha_button_site_key = site_key

    def write(self, vals):
        other_builders = self
        if vals.get('component_recaptcha_button_active'):
            xmlid_recaptcha_js = 'formio_component_recaptcha_button.formio_component_recaptcha_js_asset'
            xmlid_recaptcha_button_js = 'formio_component_recaptcha_button.formio_component_recaptcha_button_js_asset'
            recaptcha_js = self.env.ref(xmlid_recaptcha_js)
            recaptcha_button_js = self.env.ref(xmlid_recaptcha_button_js)
            for builder in self:
                extra_assets_vals = []
                has_recaptcha_js = builder._has_extra_asset(recaptcha_js)
                has_recaptcha_button_js = builder._has_extra_asset(recaptcha_button_js)
                if not has_recaptcha_js:
                    extra_assets_vals.append((4, recaptcha_js.id, 0))
                if not has_recaptcha_button_js:
                    extra_assets_vals.append((4, recaptcha_button_js.id, 0))
                if not has_recaptcha_js or not has_recaptcha_button_js:
                    builder_vals = copy(vals)
                    if not builder_vals.get('extra_asset_ids'):
                        builder_vals['extra_asset_ids'] = []
                        builder_vals['extra_asset_ids'] += extra_assets_vals
                        builder.write(builder_vals)
                        other_builders -= builder
        return super(Builder, other_builders).write(vals)
