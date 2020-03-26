# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from odoo.addons.formio.utils import get_field_selection_label


class Form(models.Model):
    _inherit = 'formio.form'

    crm_lead_id = fields.Many2one('crm.lead', readonly=True, string='CRM Lead')

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        builder = self._get_builder_from_id(vals.get('builder_id'))
        res_id = self._context.get('active_id')

        if not builder or not builder.res_model_id.model == 'crm.lead' or not res_id:
            return vals

        vals['crm_lead_id'] = res_id
        return vals

    @api.depends('crm_lead_id', 'crm_lead_id.partner_id')
    def _compute_res_fields(self):
        super(Form, self)._compute_res_fields()
        for r in self:
            if r.res_model == 'crm.lead' and r.res_id:
                lead = self.env['crm.lead'].search([('id', '=', r.res_id)])
                r.res_partner_id = r.crm_lead_id.partner_id

                action = self.env.ref('crm.crm_lead_opportunities_tree_view')
                url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                    id=r.res_id,
                    model='crm.lead',
                    action=action.id)
                r.res_act_window_url = url
                r.res_name = r.res_model_name
                r.res_info = '%s / %s / %s' % (r.res_model_name, r.crm_lead_id.stage_id.name, r.crm_lead_id.name)

    @api.onchange('builder_id')
    def _onchange_builder_domain(self):
        res = super(Form, self)._onchange_builder_domain()
        if self._context.get('active_model') == 'crm.lead':
            res_model_id = self.env.ref('crm.model_crm_lead').id
            domain = [
                ('state', '=', BUILDER_STATE_CURRENT),
                ('res_model_id', '=', res_model_id),
            ]
            res['domain'] = {'builder_id': domain}
        return res
