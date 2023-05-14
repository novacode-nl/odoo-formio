# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class ExtraAsset(models.Model):
    _name = 'formio.extra.asset'
    _inherit = ['mail.thread']
    _description = 'formio.js Extra Asset'
    _order = 'sequence'
    _rec_name = 'attachment_id'

    type = fields.Selection(
        [("js", "js"), ("css", "css"), ("image", "image"), ("license", "license")],
        string="Type",
        required=True,
        tracking=True
    )
    target = fields.Selection(
        [('append', 'Append'), ('prepend', 'Prepend')],
        string="Target",
        required=True,
        tracking=True,
        help="Target: append (after) or prepend (before) formio.js, OWL, jQuery"
    )
    attachment_id = fields.Many2one(
        'ir.attachment', string="Attachment",
        required=True,
        ondelete='cascade',
        tracking=True,
        # don't allow to relink attachments (hence domain), but field is needed to create new attachment
        domain=[('id', '=', 0)],
        context={'default_res_model': 'formio.extra.asset'})
    attachment_type = fields.Selection(related='attachment_id.type', string='Attachment Type', readonly=True)
    attachment_public = fields.Boolean(related='attachment_id.public', string='Attachment Public', readonly=True)
    attachment_formio_ref = fields.Char(related='attachment_id.formio_ref', string='Forms Ref', readonly=True)
    sequence = fields.Integer(string='Sequence', default=1, tracking=True,)
    url = fields.Char(string="URL", compute='_compute_url')

    @api.model_create_multi
    def create(self, vals_list):
        # Workaround, put link with attachment_id.
        # Wtf, Odoo only stores res_id when attachement_id.public is False
        res = super().create(vals_list)
        for rec in res:
            vals = {'res_id': rec.id}
            rec.attachment_id.write(vals)
        return res

    @api.depends('attachment_id')
    def _compute_url(self):
        for r in self:
            if r.attachment_type == 'url':
                r.url = r.attachment_id.url
            elif r.attachment_type == 'binary':
                if r.type == 'image':
                    r.url = '/web/image/{attachment_id}'.format(attachment_id=r.attachment_id.id)
                else:
                    r.url = '/web/content/{attachment_id}/{name}'.format(
                        attachment_id=r.attachment_id.id,
                        name=r.attachment_id.name)
            else:
                r.url = False

    def unlink(self):
        self.mapped('attachment_id').unlink()
        return super(ExtraAsset, self).unlink()
