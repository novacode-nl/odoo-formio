# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class Form(models.Model):
    _inherit = 'formio.form'

    report_ids = fields.One2many('formio.builder.report', related='builder_id.report_ids')
    report_print_wizard_ids = fields.One2many('formio.builder.report', compute='_compute_report_print_wizards')
    reports_print_wizard_count = fields.Integer(compute='_compute_report_print_wizards')

    @api.depends('builder_id')
    def _compute_report_print_wizards(self):
        self.report_print_wizard_ids = [(6, 0, self.builder_id.report_print_wizard_ids.ids)]
        self.reports_print_wizard_count = len(self.builder_id.report_print_wizard_ids)

    def show_components_not_implemented(self, report_name):
        """
        @param str report_name as xmlid (external ID)
        """
        domain = [('report_name', '=', report_name)]
        report = self.env['ir.actions.report'].sudo().search(domain, limit=1)
        report_config = self.builder_id.sudo().report_ids.filtered(lambda x: x.ir_actions_report_id.id == report.id)
        return report_config.show_components_not_implemented

    def action_report_wizard(self):
        reports_print_wizard = self.builder_id.report_print_wizard_ids.filtered(lambda x: x.report_type == 'qweb-pdf')
        if reports_print_wizard:
            Wiz = self.env['formio.form.report.qweb.wizard']
            vals = {'formio_form_id': self.id, 'wizard_line_ids': []}

            for r in reports_print_wizard:
                line_vals = {
                    'ir_actions_report_id': r.ir_actions_report_id.id,
                    'print_report': r.default_enable
                }
                vals['wizard_line_ids'].append((0, 0, line_vals))
            wiz = Wiz.create(vals)
            return {
                'name': _('Print Reports'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'formio.form.report.qweb.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': wiz.id
            }
