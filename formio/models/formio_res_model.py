# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class ResModel(models.Model):
    _name = 'formio.res.model'
    _description = 'Formio Resource Model'

    _rec_name = 'ir_model_id'

    ir_model_id = fields.Many2one('ir.model')
    module_dependency = fields.Boolean()

    @api.multi
    def unlink(self):
        if not self.module_dependency:
            return super(ResModel, self).unlink()
        else:
            raise UserError(_("Can't unlink because of module dependency!"))
