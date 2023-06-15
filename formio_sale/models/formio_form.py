# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class Form(models.Model):
    _inherit = 'formio.form'

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale Order", readonly=True, ondelete="cascade"
    )

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        builder = self._get_builder_from_id(vals.get('builder_id'))
        res_id = self._context.get('active_id')

        if not builder or not builder.res_model_id.model == 'sale.order' or not res_id:
            return vals

        sale_order = self.env['sale.order'].search([('id', '=', res_id)])
        vals['sale_order_id'] = res_id
        vals['res_partner_id'] = sale_order.partner_id.id

        if sale_order.state in ('draft', 'sent'):
            action = self.env.ref('sale.action_quotations')
        else:
            action = self.env.ref('sale.action_orders')
        url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
            id=res_id,
            model='sale.order',
            action=action.id)

        vals['res_act_window_url'] = url
        vals['res_name'] = sale_order.name
        return vals

    def _get_builder_id_domain(self):
        self.ensure_one()
        domain = super()._get_builder_id_domain()
        if self._context.get('active_model') == 'sale.order':
            res_model_id = self.env.ref('sale.model_sale_order').id
            domain.append(('res_model_id', '=', res_model_id))
        return domain
