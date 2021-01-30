# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class FormioBuilderReportPrintWizardConfig(models.Model):
    _name = 'formio.builder.report.print.wizard.config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Form Builder Report Print Wizard Config'
    _order = 'sequence, id'

    sequence = fields.Integer(
        default=1, help="Report priority/sequence for the Builder Form"
    )
    builder_id = fields.Many2one('formio.builder', string='Form Builder', tracking=True)
    ir_actions_report_id = fields.Many2one(
        'ir.actions.report', string='Report', tracking=True,
        domain=[('model', '=', 'formio.form'), ('report_type', '=', 'qweb-pdf')])
    builder_report_ids = fields.One2many(
        'ir.actions.report', compute='_compute_builder_report_ids')
    report_type = fields.Selection(related='ir_actions_report_id.report_type')
    report_name = fields.Char(related='ir_actions_report_id.name')
    default_enable = fields.Boolean(
        "Default Enable", tracking=True)

    @api.depends('builder_id', 'ir_actions_report_id')
    def _compute_builder_report_ids(self):
        for r in self:
            r.builder_report_ids = [(6, 0, r.builder_id.report_print_wizard_ids.ir_actions_report_id.ids)]
