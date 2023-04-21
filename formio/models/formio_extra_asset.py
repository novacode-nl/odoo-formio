# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class ExtraAsset(models.Model):
    _name = 'formio.extra.asset'
    _description = 'formio.js Extra Asset'
    _order = 'sequence'
    _rec_name = 'attachment_id'

    type = fields.Selection([('js', 'js'), ('css', 'css'), ('license', 'license')], string='Type', required=True)
    attachment_id = fields.Many2one(
        'ir.attachment', string="Attachment",
        required=True, ondelete='cascade', domain=[('res_model', '=', 'formio.extra.asset')],
        context={'default_res_model': 'formio.extra.asset'})
    attachment_type = fields.Selection(related='attachment_id.type', string='Attachment Type', readonly=True)
    sequence = fields.Integer(string='Sequence', default=1)
    url = fields.Char(compute='_compute_url')

    @api.depends('attachment_id')
    def _compute_url(self):
        for r in self:
            if r.attachment_type == 'url':
                r.url = r.attachment_id.url
            elif r.attachment_type == 'binary':
                r.url = '/web/content/{attachment_id}/{name}'.format(
                    attachment_id=r.attachment_id.id,
                    name=r.attachment_id.name)
            else:
                r.url = False

    def unlink(self):
        self.mapped('attachment_id').unlink()
        return super(ExtraAsset, self).unlink()
