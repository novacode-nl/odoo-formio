# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from odoo.addons.formio.utils import get_field_selection_label


class Form(models.Model):
    _inherit = 'formio.form'

    base_res_partner_id = fields.Many2one('res.partner', readonly=True, string='Partner')

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        builder = self._get_builder_from_id(vals.get('builder_id'))
        res_id = self._context.get('active_id')

        if not builder or not builder.res_model_id.model == 'res.partner' or not res_id:
            return vals

        partner = self.env['res.partner'].browse(res_id)
        action = self.env.ref('contacts.action_contacts')
        url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
            id=res_id,
            model='res.partner',
            action=action.id)
        res_model_name = builder.res_model_id.name

        vals['res_act_window_url'] = url
        vals['res_info'] = partner.name
        vals['base_res_partner_id'] = res_id
        vals['res_partner_id'] = res_id
        return vals

    @api.onchange('builder_id')
    def _onchange_builder_domain(self):
        res = super(Form, self)._onchange_builder_domain()
        if self._context.get('active_model') == 'res.partner':
            res_model_id = self.env.ref('base.model_res_partner').id
            domain = [
                ('state', '=', BUILDER_STATE_CURRENT),
                ('res_model_id', '=', res_model_id),
            ]
            res['domain'] = {'builder_id': domain}
        return res
