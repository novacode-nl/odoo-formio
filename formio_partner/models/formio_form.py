# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import models


class Form(models.Model):
    _inherit = 'formio.form'

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        builder = self._get_builder_from_id(vals.get('builder_id'))
        res_id = self._context.get('active_id')

        if not builder or not builder.res_model_id.model == 'res.partner':
            return vals

        partner = self.env['res.partner'].browse(res_id)
        action = self.env.ref('contacts.action_contacts')
        url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
            id=res_id,
            model='res.partner',
            action=action.id)

        vals['res_act_window_url'] = url
        vals['res_name'] = partner.name
        vals['partner_id'] = res_id
        vals['res_partner_id'] = res_id
        return vals

    def _get_builder_id_domain(self):
        self.ensure_one()
        domain = super()._get_builder_id_domain()
        if self._context.get('active_model') == 'res.partner':
            res_model_id = self.env.ref('base.model_res_partner').id
            domain.append(('res_model_id', '=', res_model_id))
        return domain
