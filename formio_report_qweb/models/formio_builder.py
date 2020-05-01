# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class Builder(models.Model):
    _inherit = 'formio.builder'

    report_ids = fields.One2many('formio.builder.report', "builder_id", string="Reports")
