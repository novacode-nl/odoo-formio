# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from flectra import api, fields, models, _
from flectra.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from flectra.addons.formio.utils import get_field_selection_label


class Form(models.Model):
    _inherit = 'formio.form'

    crm_lead_id = fields.Many2one(
        'crm.lead', compute='_compute_crm_lead_id', store=True,
        readonly=True, string='Sale Order')

    @api.one
    @api.depends('res_model_id', 'res_id')
    def _compute_crm_lead_id(self):
        if self._context.get('active_model') == 'crm.lead':
            lead = self.env['crm.lead'].search([('id', '=', self.res_id)])
            self.crm_lead_id = lead.id

    @api.one
    @api.depends('res_model_id', 'res_id')
    def _compute_partner_id(self):
        super(Form, self)._compute_partner_id()
        if self._context.get('active_model') == 'crm.lead':
            self.partner_id = self.crm_lead_id.partner_id

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

    def _compute_res_fields(self):
        super(Form, self)._compute_res_fields()
        for r in self:
            if r.res_model_id.model == 'crm.lead':
                action = self.env.ref('crm.action_crm_tag_form_view_oppor11')
                url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                    id=r.res_id,
                    model='crm.lead',
                    action=action.id)
                r.res_act_window_url = url
                r.res_name = r.res_model_name
                r.res_info = r.crm_lead_id.stage_id.name

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
