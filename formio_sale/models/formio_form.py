# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from odoo.addons.formio.utils import get_field_selection_label


class Form(models.Model):
    _inherit = 'formio.form'

    sale_order_id = fields.Many2one(
        'sale.order', compute='_compute_res_fields', store=True,
        readonly=True, string='Sale Order')

    @api.depends('res_model_id', 'res_id')
    def _compute_res_fields(self):
        compute = super(Form, self)._compute_res_fields()
        if not compute:
            return False

        for r in self:
            if r.res_model == 'sale.order' and r.res_id:
                order = self.env['sale.order'].search([('id', '=', r.res_id)])
                r.sale_order_id = order.id
                r.res_partner_id = order.partner_id.id
                if order.state in ('draft', 'sent'):
                    action = self.env.ref('sale.action_quotations')
                else:
                    action = self.env.ref('sale.action_orders')

                url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                    id=r.res_id,
                    model='sale.order',
                    action=action.id)
                r.res_act_window_url = url
                r.res_name = order.name
                r.res_info = get_field_selection_label(order, 'state')

    @api.onchange('builder_id')
    def _onchange_builder_id(self):
        res = {}
        if self._context.get('active_model') == 'sale.order':
            res_model_id = self.env.ref('sale.model_sale_order').id
            domain = [
                ('state', '=', BUILDER_STATE_CURRENT),
                ('res_model_id', '=', res_model_id),
            ]
            res['domain'] = {'builder_id': domain}
        return res

    @api.multi
    def action_open_res_act_window(self):
        if self.res_model_id.model == 'sale.order':
            if self.sale_order_id.state in ('draft', 'sent'):
                action = self.env.ref('sale.action_quotations')
            else:
                action = self.env.ref('sale.action_orders')

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            "views": [[False, "form"]],
        }
