# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BuilderTranslation(models.Model):
    _name = 'formio.builder.translation'
    _description = 'formio.builder Translation'
    _order = 'builder_name ASC, builder_version DESC, lang_name ASC, source ASC'

    builder_id = fields.Many2one(
        'formio.builder', string='Form Builder', required=True, ondelete='cascade')
    lang_id = fields.Many2one('res.lang', string='Language', required=True)
    source_property = fields.Text(string='Source Property')
    source = fields.Text(string='Source Text', required=True)
    value = fields.Text(string='Translated Value', required=True)

    # related fields
    builder_name = fields.Char(related='builder_id.name', string='Builder Name', store=True)
    builder_version = fields.Integer(related='builder_id.version', string='Builder Version', store=True)
    lang_name = fields.Char(related='lang_id.name', string='Language Name', store=True)

    @api.constrains('builder_id', 'lang_id', 'source')
    def _constraint_unique(self):
        errors = []
        for rec in self:
            res = self.search([
                ("builder_id", "=", rec.builder_id.id),
                ("lang_id", "=", rec.lang_id.id),
                ("source", "=", rec.source)
            ])
            if len(res) > 1:
                errors.append(
                    _("- Form Builder Name: {name}\n- Source Term: {source}\n- Translation: {translation}").format(
                        name=rec.builder_id.name, source=rec.source, translation=rec.value
                    )
                )
        if errors:
            msg = _('Form Builder Translations must be unique.\n\n%s') % '\n\n'.join(errors)
            raise ValidationError(msg)

    @api.depends('lang_id', 'source', 'value')
    def name_get(self):
        res = []
        for r in self:
            name = '{lang}: {source} => {value}'.format(
                lang=r.lang_id, source=r.source, value=r.value
            )
            res.append((r.id, name))
        return res
