# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class ResLang(models.Model):
    _inherit = 'res.lang'

    formio_ietf_code = fields.Char(compute='_compute_formio_ietf_code', string='IETF Code')
    formio_short_code = fields.Char(
        compute='_compute_formio_short_code', store=True,
        string='Short Code')

    def _compute_formio_ietf_code(self):
        for lang in self:
            lang.formio_ietf_code = self._formio_ietf_code(lang.code)

    @api.depends('code')
    def _compute_formio_short_code(self):
        for lang in self:
            lang.formio_short_code = lang.code[0:2]

    @api.model
    def _formio_ietf_code(self, code):
        return code.replace('_', '-')

    @api.model
    def _from_formio_ietf_code(self, code):
        return code.replace('-', '_')
