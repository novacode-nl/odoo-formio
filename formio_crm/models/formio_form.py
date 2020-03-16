# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from odoo.addons.formio.utils import get_field_selection_label


class Form(models.Model):
    _inherit = 'formio.form'

    crm_lead_id = fields.Many2one(
        'crm.lead', compute='_compute_res_fields', store=True,
        readonly=True, string='CRM Lead')

    @api.one
    @api.depends('res_model_id', 'res_id')
    def _compute_res_fields(self):
        super(Form, self)._compute_res_fields()
        if self.res_model == 'crm.lead':
            lead = self.env['crm.lead'].search([('id', '=', self.res_id)])
            self.crm_lead_id = lead.id
            self.res_partner_id = self.crm_lead_id.partner_id

            action = self.env.ref('crm.action_crm_tag_form_view_oppor11')
            url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                id=self.res_id,
                model='crm.lead',
                action=action.id)
            self.res_act_window_url = url
            self.res_name = self.res_model_name
            self.res_info = self.crm_lead_id.stage_id.name

    @api.onchange('builder_id')
    def _onchange_builder_id(self):
        res = super(Form, self)._onchange_builder_id()
        if self._context.get('active_model') == 'crm.lead':
            res_model_id = self.env.ref('crm.model_crm_lead').id
            domain = [
                ('state', '=', BUILDER_STATE_CURRENT),
                ('res_model_id', '=', res_model_id),
            ]
            res['domain'] = {'builder_id': domain}
        return res

    @api.multi
    def action_open_res_act_window(self):
        res = super(Form, self).action_open_res_act_window()
        if self._context.get('active_model') == 'crm.lead':
            res = {
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': self.crm_lead_id.id,
                "views": [[False, "form"]],
            }
        return res
