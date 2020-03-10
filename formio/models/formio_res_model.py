# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from flectra import api, fields, models, _
from flectra.exceptions import UserError


class ResModel(models.Model):
    _name = 'formio.res.model'
    _description = 'Formio Resource Model'

    _rec_name = 'ir_model_id'

    ir_model_id = fields.Many2one('ir.model', string='Model')
    module_dependency = fields.Boolean(readonly=True)

    @api.multi
    def unlink(self):
        if not self.module_dependency:
            return super(ResModel, self).unlink()
        else:
            raise UserError(_("Can't unlink because this record is a module dependency!"))
