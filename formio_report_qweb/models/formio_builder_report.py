# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class FormioBuilderReport(models.Model):
    _name = 'formio.builder.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Formio Builder Reports'

    builder_id = fields.Many2one('formio.builder', string='Form Builder', tracking=True)
    ir_actions_report_id = fields.Many2one(
        'ir.actions.report', string='Report', tracking=True,
        domain=[('model', '=', 'formio.form')])
    show_components_not_implemented = fields.Boolean(
        "Show not implemented components", tracking=True)
