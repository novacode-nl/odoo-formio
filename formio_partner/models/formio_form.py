# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from odoo.addons.formio.utils import get_field_selection_label


class Form(models.Model):
    _inherit = 'formio.form'

    base_res_partner_id = fields.Many2one(
        'res.partner', compute='_compute_res_fields', store=True,
        readonly=True, string='Partner')

    @api.one
    @api.depends('res_model_id', 'res_id')
    def _compute_res_fields(self):
        super(Form, self)._compute_res_fields()
        if self.res_model == 'res.partner':
            partner = self.env['res.partner'].search([('id', '=', self.res_id)])
            self.base_res_partner_id = partner.id
            self.base_partner_id = partner.id

            action = self.env.ref('contacts.action_contacts')
            url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                id=self.res_id,
                model='res.partner',
                action=action.id)
            self.res_act_window_url = url
            self.res_name = self.res_model_name
            self.res_info = partner.name

    @api.onchange('builder_id')
    def _onchange_builder_id(self):
        res = super(Form, self)._onchange_builder_id()
        if self._context.get('active_model') == 'res.partner':
            res_model_id = self.env.ref('base.model_res_partner').id
            domain = [
                ('state', '=', BUILDER_STATE_CURRENT),
                ('res_model_id', '=', res_model_id),
            ]
            res['domain'] = {'builder_id': domain}
        return res

    @api.multi
    def action_open_res_act_window(self):
        res = super(Form, self).action_open_res_act_window()
        if self.res_model_id.model == 'res.partner':
            res = {
                'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'res_id': self.base_res_partner_id.id,
                "views": [[False, "form"]],
            }
        return res
