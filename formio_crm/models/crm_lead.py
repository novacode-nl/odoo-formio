# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    formio_forms = fields.One2many('formio.form', 'crm_lead_id', string='Form.io Forms')
    formio_forms_count = fields.Integer(compute='_compute_formio_forms_count')
    formio_this_model_id = fields.Many2one('ir.model', compute='_compute_formio_this_model_id')

    def _compute_formio_forms_count(self):
        for r in self:
            r.formio_forms_count = len(r.formio_forms)

    def _compute_formio_this_model_id(self):
        self.ensure_one()
        model_id = self.env.ref('crm.model_crm_lead').id
        self.formio_this_model_id = model_id

    @api.multi
    def action_formio_forms(self):
        self.ensure_one()
        res_model_id = self.env.ref('base.model_res_partner').id
        return {
            'name': 'Forms.io',
            'type': 'ir.actions.act_window',
            'domain': [('res_id', '=', self.id), ('res_model_id', '=', res_model_id)],
            'context': {'default_res_id': self.id},
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'formio.form',
            'view_id': False,
        }

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(CrmLead, self)._onchange_partner_id()
        for r in self.formio_forms:
            if r.res_model == 'crm.lead':
                r.res_partner_id = self.partner_id
