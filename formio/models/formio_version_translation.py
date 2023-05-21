# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class VersionTranslation(models.Model):
    _name = 'formio.version.translation'
    _description = 'formio.js Version Translation'
    _order = 'lang_id ASC'

    formio_version_id = fields.Many2one('formio.version', string='formio.js version', required=True)
    base_translation_id = fields.Many2one(
        'formio.translation', string='formio.js base translation', ondelete='set null'
    )
    lang_id = fields.Many2one('res.lang', string='Language', required=True)
    source_property = fields.Text(
        string='Property',
        help="A formio.js library translation property, eg 'submit', 'cancel', 'error', 'previous'"
    )
    source_text = fields.Text(string='Source Text', required=True)
    value = fields.Text(string='Translation Value', required=True)

    @api.depends('lang_id', 'source_id', 'value')
    def name_get(self):
        res = []
        for r in self:
            name = '{lang}: {source} => {value}'.format(
                lang=r.lang_id, source=r.source_id.source, value=r.value
            )
            res.append((r.id, name))
        return res
