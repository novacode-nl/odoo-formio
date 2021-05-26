# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models
from odoo.http import request


class Form(models.Model):
    _inherit = 'formio.form'

    website_visitor_id = fields.Many2one('website.visitor')

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        if not vals.get('submission_timezone') and request:
            visitor_obj = self.env['website.visitor']
            if not request.env.user:
                visitor_obj = visitor_obj.with_user(request.env.ref('base.public_user'))
            visitor = visitor_obj._get_visitor_from_request()
            if visitor:
                vals['website_visitor_id'] = visitor.id
                vals['submission_timezone'] = visitor.timezone
        return vals
