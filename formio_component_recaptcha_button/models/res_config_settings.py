# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    formio_recaptcha_button_site_key = fields.Char(string='formio_recaptcha_button Site Key', config_parameter='formio_recaptcha_button.site_key')
    formio_recaptcha_button_secret_key = fields.Char(string='formio_recaptcha_button Secret Key', config_parameter='formio_recaptcha_button.secret_key')
