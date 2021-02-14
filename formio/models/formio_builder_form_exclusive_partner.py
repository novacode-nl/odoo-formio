# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BuilderFormExclusivePartner(models.Model):
    _name = 'formio.builder.form.exclusive.partner'
    _description = 'Form Builder Form Exclusive Partner'

    builder_id = fields.Many2one('formio.builder', string='Form Builder', required=True)
    builder_uuid = fields.Char(related='builder_id.uuid', string='Form Builder UUID')
    builder_title = fields.Char(related='builder_id.title', string='Form Builder Title')
    builder_name = fields.Char(related='builder_id.name', string='Form Builder Name')
    builder_version = fields.Integer(related='builder_id.version', string='Form Builder Version')
    builder_state = fields.Selection(related='builder_id.state', string='Form Builder State')
    partner_id = fields.Many2one('res.partner', required=True)
    partner_parent_id = fields.Many2one('res.partner', related='partner_id.parent_id')
    #partner_child_ids = fields.One2many('res.partner', related='partner_id.child_ids')
    partner_company_type = fields.Selection(related='partner_id.company_type')

    @api.constrains('builder_id', 'partner_id')
    def _constraint_unique_builder_and_partner(self):
        for r in self:
            res = self.search([
                ("builder_id", "=", r.builder_id.id),
                ("partner_id", "=", r.partner_id.id)
            ])
            if len(res) > 1:
                msg = _("A Form Builder can only be exclusively assigned to a Partner once. Affected Form Builder:\n%s") % r.builder_id.display_name_full
                raise ValidationError(msg)
