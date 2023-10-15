# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64
import io

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FormReportQwebWizard(models.TransientModel):
    _name = 'formio.form.report.qweb.wizard'
    _description = "Form Report QWeb Wizard"

    formio_form_id = fields.Many2one('formio.form', required=True)
    wizard_line_ids = fields.One2many('formio.form.report.qweb.wizard.line', 'wizard_id')
    print_count = fields.Integer(compute='_compute_wizard_data')
    save_attachment = fields.Boolean(string='Save as Attachment')
    datas = fields.Binary(string='File Content (base64)')

    @api.depends('wizard_line_ids')
    def _compute_wizard_data(self):
        for wiz in self:
            wiz.print_count = len(wiz.wizard_line_ids.filtered('print_report'))

    def action_print(self):
        filename = self._generate_qweb_report()
        return {
            'type' : 'ir.actions.act_url',
            'url': '/web/content/formio.form.report.qweb.wizard/%s/datas/%s' % (self.id, filename),
            'target': 'self',
        }

    def action_save_attachment(self):
        self._generate_qweb_report()

    def _generate_qweb_report(self):
        def close_streams(streams):
            for stream in streams:
                try:
                    stream.close()
                except Exception:
                    pass

        if not self.wizard_line_ids:
            raise UserError(_('Please close and try again.\nRecord for the print wizard does not exist anymore.'))

        wizard_lines = self.wizard_line_ids.filtered(lambda x: x.print_report)
        IrReport = self.env['ir.actions.report']
        formio_forms = self.env['formio.form']

        streams = []
        report_names = []
        for line in wizard_lines:
            formio_form = line.wizard_id.formio_form_id
            formio_forms |= formio_form
            report = line.ir_actions_report_id
            content, report_type = report._render([formio_form.id])

            if report_type == 'pdf':
                pdf_content_stream = io.BytesIO(content)
                streams.append(pdf_content_stream)
                report_names.append(line.ir_actions_report_id.name)

        if streams:
            result = IrReport._merge_pdfs(streams)
            close_streams(streams)
            vals = {'datas': base64.b64encode(result)}

            current_datetime = fields.Datetime.context_timestamp(self, fields.Datetime.now())
            # colons ':' get converted to whitespace, hence convert to dashes '-'
            current_datetime_str = fields.Datetime.to_string(current_datetime).replace(':', '-')
            filename = '%s - %s' % (' - '.join(report_names), current_datetime_str)

            if self.save_attachment:
                attach_vals = {
                    'name': filename,
                    'res_model': 'formio.form',
                    'res_id': self.formio_form_id.id
                }
                attach_vals.update(vals)
                self.env['ir.attachment'].create(attach_vals)
            self.write(vals)
            return filename
        else:
            raise UserError(_('The report could not be generated. It is recommended to check the server log.'))


class FormReportQwebWizardLine(models.TransientModel):
    _name = 'formio.form.report.qweb.wizard.line'
    _description = "Form Report QWeb Wizard Line"

    wizard_id = fields.Many2one('formio.form.report.qweb.wizard', required=True)
    ir_actions_report_id = fields.Many2one('ir.actions.report', string='Report', required=True)
    print_report = fields.Boolean(default=True, string='Print')
