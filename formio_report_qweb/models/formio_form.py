# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class Form(models.Model):
    _inherit = 'formio.form'

    def show_components_not_implemented(self, report_name):
        """
        @param str report_name as xmlid (external ID)
        """
        domain = [('report_name', '=', report_name)]
        report = self.env['ir.actions.report'].search(domain, limit=1)
        report_config = self.builder_id.report_ids.filtered(lambda x: x.ir_actions_report_id.id == report.id)
        return report_config.show_components_not_implemented
