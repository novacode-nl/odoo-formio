# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class IrActionsReportXml(models.Model):
    _inherit = 'ir.actions.report'

    formio_builder_report_ids = fields.One2many(
        'formio.builder.report', 'ir_actions_report_id', string='Form Builder Reports')
