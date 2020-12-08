# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class UnsanitizeHtmlField(models.Model):
    _name = 'website.editor.unsanitize.html.field'
    _description = 'Unsanitize HTML Field (for Model)'

    ir_model_id = fields.Many2one("ir.model", string="Select Model")
    ir_model_field_id = fields.Many2one("ir.model.fields", string="Select Field")    
    model = fields.Char(string='Model', required=True)
    field = fields.Char(string='Field', required=True)
    model_field = fields.Char(string='Model Field', compute='_compute_model_field', store=True)
    active = fields.Boolean(string='Active', default=False)

    @api.depends('model', 'field')
    def _compute_model_field(self):
        for r in self:
            if r.model and r.field:
                r.model_field = '%s.%s' % (r.model, r.field)

    @api.onchange('ir_model_id')
    def _onchange_ir_model_id(self):
        res = {}
        self.ir_model_field_id = False
        
        if self.ir_model_id:
            self.model = self.ir_model_id.model
            res['domain'] = {'ir_model_field_id': [('model_id', '=', self.ir_model_id.id)]}
        else:
            res['domain'] = {'ir_model_field_id': [('id', '=', False)]}
        return res

    @api.onchange('ir_model_field_id')
    def _onchange_ir_model_field_id(self):
        if self.ir_model_field_id:
            self.field = self.ir_model_field_id.name

