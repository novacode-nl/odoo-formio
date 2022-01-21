# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    formio_forms = fields.One2many('formio.form', 'sale_order_id', string='Forms')
    formio_forms_count = fields.Integer(
        compute='_compute_formio_forms_count', compute_sudo=True, string='Forms Count')
    formio_this_model_id = fields.Many2one(
        'ir.model', compute_sudo=True, compute='_compute_formio_this_model_id')

    def _compute_formio_forms_count(self):
        for r in self:
            r.formio_forms_count = len(r.formio_forms)

    def _compute_formio_this_model_id(self):
        self.ensure_one()
        model_id = self.env.ref('sale.model_sale_order').id
        self.formio_this_model_id = model_id

    def write(self, vals):
        # Simpler to maintain and less risk with extending, than
        # computed field(s) in the formio.form object.
        res = super(SaleOrder, self).write(vals)
        if self.formio_forms:
            form_vals = self._prepare_write_formio_form_vals(vals)
            if form_vals:
                self.formio_forms.write(form_vals)
        return res

    def _prepare_write_formio_form_vals(self, vals):
        if vals.get('name'):
            form_vals = {
                'res_name': self.name
            }
            return form_vals
        else:
            return False

    def action_formio_forms(self):
        self.ensure_one()
        res_model_id = self.env.ref('sale.model_sale_order').id
        return {
            'name': 'Forms',
            'type': 'ir.actions.act_window',
            'domain': [('res_id', '=', self.id), ('res_model_id', '=', res_model_id)],
            'context': {'default_res_id': self.id},
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'formio.form',
            'view_id': False,
        }
