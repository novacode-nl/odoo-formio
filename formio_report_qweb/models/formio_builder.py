# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class Builder(models.Model):
    _inherit = 'formio.builder'

    report_ids = fields.One2many('formio.builder.report', "builder_id", string="Standard Reports")
    report_print_wizard_ids = fields.One2many('formio.builder.report.print.wizard.config', "builder_id", string="Print Wizard Reports")

    @api.onchange('report_print_wizard_ids')
    def _change_report_print_wizard_ids(self):
        for wiz in self.report_print_wizard_ids:
            wiz.builder_report_ids = [(6, 0, self.report_print_wizard_ids.ir_actions_report_id.ids)]
