# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class VersionAsset(models.Model):
    _name = 'formio.version.asset'
    _description = 'formio.js Version Asset'
    _order = 'sequence ASC'

    version_id = fields.Many2one('formio.version', string='formio.js version', ondelete='cascade')
    type = fields.Selection(
        [
            ("js", "js"),
            ("css", "css"),
            ("license", "license"),
            ("eot", "EOT Font File"),
            ("otf", "OTF Font File"),
            ("svg", "SVG Font File"),
            ("ttf", "TTF Font File"),
            ("woff", "WOFF Font File"),
            ("woff2", "WOFF2 Font File"),
        ], string="Type", required=True)
    attachment_id = fields.Many2one(
        'ir.attachment', string="Attachment",
        required=True, ondelete='cascade', domain=[('res_model', '=', 'formio.version.asset')],
        context={'default_res_model': 'formio.version.asset'})
    attachment_type = fields.Selection(related='attachment_id.type', string='Attachment Type', readonly=True)
    attachment_formio_ref = fields.Char(related='attachment_id.formio_ref', string='Forms Ref', readonly=True)
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
                    name=r.attachment_id.name,
                )

    def unlink(self):
        self.mapped('attachment_id').unlink()
        return super(VersionAsset, self).unlink()
