# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class Form(models.Model):
    _inherit = 'formio.form'

    sale_order_id = fields.Many2one(
        'sale.order', compute='_compute_sale_order_id', store=True,
        readonly=True, string='Sale Order')
    partner_id = fields.Many2one(
        'res.partner', related='sale_order_id.partner_id',
        store=True, readonly=True, string='Partner')

    @api.one
    @api.depends('res_model_id', 'res_id')
    def _compute_sale_order_id(self):
        if self.res_model_id.model == 'sale.order':
            order = self.env['sale.order'].search([('id', '=', self.res_id)])
            self.sale_order_id = order.id

    @api.onchange('builder_id')
    def _onchange_builder_id(self):
        res = {}
        if self._context.get('active_model') == 'sale.order':
            res_model_id = self.env.ref('sale.model_sale_order').id
            res['domain'] = {'builder_id': [('res_model_id', '=', res_model_id)]}
        return res
