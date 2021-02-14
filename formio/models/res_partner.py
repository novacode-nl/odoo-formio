# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    exclusive_formio_builder_form_rel_ids = fields.One2many(
        'formio.builder.form.exclusive.partner', 'partner_id',
        string='Exclusive Forms',
        help='Give access only to Forms this partner (either linked directly to the partner or to its children). If left empty, this restriction doesn\'t apply.')
    exclusive_formio_builder_form_ids = fields.One2many(
        'formio.builder.form.exclusive.partner', compute='_compute_exclusive_formio_builder_form_ids', string='Exclusive Forms determined')

    def _compute_exclusive_formio_builder_form_ids(self):
        for r in self:
            domain = ['|', ('partner_id', '=', r.id), ('partner_id', 'parent_of', r.id)]
            res = self.env['formio.builder.form.exclusive.partner'].search(domain)

            if res:
                r.exclusive_formio_builder_form_ids = [(6, 0, res.ids)]
            else:
                r.exclusive_formio_builder_form_ids = False
