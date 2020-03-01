# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from odoo.addons.formio.utils import get_field_selection_label


class Form(models.Model):
    _inherit = 'formio.form'

    @api.one
    @api.depends('res_model_id', 'res_id')
    def _compute_partner_id(self):
        super(Form, self)._compute_partner_id()
        if self.res_model_id.model == 'res.partner':
            partner = self.env['res.partner'].search([('id', '=', self.res_id)])
            self.partner_id = partner.id

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

    def _compute_res_fields(self):
        super(Form, self)._compute_res_fields()
        for r in self:
            if r.res_model_id.model == 'res.partner':
                action = self.env.ref('base.action_partner_form')
                url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                    id=r.res_id,
                    model='res.partner',
                    action=action.id)
                r.res_act_window_url = url
                r.res_name = r.res_model_name
                r.res_info = r.partner_id.name

    @api.multi
    def action_open_res_act_window(self):
        res = super(Form, self).action_open_res_act_window()
        if self._context.get('active_model') == 'res.partner':
            res = {
                'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'res_id': self.partner_id.id,
                "views": [[False, "form"]],
            }
        return res
