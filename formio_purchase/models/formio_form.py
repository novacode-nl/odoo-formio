# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT


class Form(models.Model):
    _inherit = 'formio.form'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', readonly=True)

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        builder = self._get_builder_from_id(vals.get('builder_id'))
        res_id = self._context.get('active_id')

        if not builder or not builder.res_model_id.model == 'purchase.order' or not res_id:
            return vals

        purchase = self.env['purchase.order'].search([('id', '=', res_id)])
        vals['purchase_order_id'] = res_id
        vals['res_partner_id'] = purchase.partner_id.id

        if purchase.state in ('draft', 'sent', 'to_approve'):
            action = self.env.ref('purchase.purchase_rfq')
        else:
            action = self.env.ref('purchase.purchase_form_action')
        url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
            id=res_id,
            model='purchase.order',
            action=action.id)

        vals['res_act_window_url'] = url
        vals['res_name'] = purchase.name
        return vals

    @api.onchange('builder_id')
    def _onchange_builder_domain(self):
        res = super(Form, self)._onchange_builder_domain()
        if self._context.get('active_model') == 'purchase.order':
            res_model_id = self.env.ref('purchase.model_purchase_order').id
            domain = [
                ('state', '=', BUILDER_STATE_CURRENT),
                ('res_model_id', '=', res_model_id),
            ]
            res['domain'] = {'builder_id': domain}
        return res
