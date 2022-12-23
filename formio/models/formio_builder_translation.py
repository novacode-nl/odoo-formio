# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class BuilderTranslation(models.Model):
    _name = 'formio.builder.translation'
    _description = 'formio.builder Translation'
    _order = 'builder_name ASC, builder_version DESC, lang_name ASC, source ASC'

    builder_id = fields.Many2one(
        'formio.builder', string='Form Builder', required=True, ondelete='cascade')
    lang_id = fields.Many2one('res.lang', string='Language', required=True)
    source = fields.Text(string='Source Term', required=True)
    value = fields.Text(string='Translated Value', required=True)

    # related fields
    builder_name = fields.Char(related='builder_id.name', string='Builder Name', store=True)
    builder_version = fields.Integer(related='builder_id.version', string='Builder Version', store=True)
    lang_name = fields.Char(related='lang_id.name', string='Language Name', store=True)

    @api.depends('lang_id', 'source', 'value')
    def name_get(self):
        res = []
        for r in self:
            name = '{lang}: {source} => {value}'.format(
                lang=r.lang_id, source=r.source, value=r.value
            )
            res.append((r.id, name))
        return res
