# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class VersionTranslation(models.Model):
    _name = 'formio.version.translation'
    _description = 'formio.js Version Translation'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence', default=1)
    formio_version_id = fields.Many2one('formio.version', string='formio.js version', required=True, ondelete='cascade')
    base_translation_id = fields.Many2one(
        'formio.translation', string='formio.js base translation', ondelete='set null'
    )
    base_translation_origin = fields.Boolean(
        string='Origin Base', default=False, compute='_compute_base_translation_origin', store=True
    )
    base_translation_updated = fields.Boolean(string='Updated Base', default=False, readonly=True)
    lang_id = fields.Many2one('res.lang', string='Language', required=True)
    source_property = fields.Text(
        string='Property',
        help="A formio.js library translation property, eg 'submit', 'cancel', 'error', 'previous'"
    )
    source_text = fields.Text(string='Source Text', required=True)
    value = fields.Text(string='Translation Value', required=True)

    @api.depends('base_translation_id')
    def _compute_base_translation_origin(self):
        for r in self:
            if r.base_translation_id:
                r.base_translation_origin = True
            else:
                r.base_translation_origin = False

    def _compute_display_name(self):
        for r in self:
            r.display_name = '{lang}: {source} => {value}'.format(
                lang=r.lang_id.code, source=r.source_id.source, value=r.value
            )

    def write(self, vals):
        base_translation_updates = self.env['formio.version.translation']
        other_updates = self.env['formio.version.translation']
        if 'lang_id' in vals or 'source_property' in vals or 'source_text' in vals or 'value' in vals:
            for rec in self:
                if rec.base_translation_origin:
                    base_translation_updates |= rec
                else:
                    other_updates |= rec
            res_other = True
            res_base = True
            if other_updates:
                res_other = super(VersionTranslation, other_updates).write(vals)
            if base_translation_updates:
                vals['base_translation_updated'] = True
                res_base = super(VersionTranslation, base_translation_updates).write(vals)
            return res_other and res_base
        else:
            return super().write(vals)
