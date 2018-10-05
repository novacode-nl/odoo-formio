# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    formio_forms = fields.One2many('formio.form', 'sale_order_id', string='Form.io Forms')
    formio_forms_count = fields.Integer(compute='_compute_formio_forms_count')

    def _compute_formio_forms_count(self):
        for r in self:
            self.formio_forms_count = len(r.formio_forms)

    @api.multi
    def action_formio_forms(self):
        self.ensure_one()
        res_model_id = self.env.ref('sale.model_sale_order').id
        return {
            'name': 'Forms.io',
            'type': 'ir.actions.act_window',
            'domain': [('res_id', '=', self.id), ('res_model_id', '=', res_model_id)],
            'context': {'default_res_id': self.id},
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'formio.form',
            'view_id': False,
        }
