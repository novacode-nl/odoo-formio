# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class Version(models.Model):
    _name = 'formio.version'
    _description = 'formio.js Version'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence DESC'

    name = fields.Char(
        "Name", required=True, tracking=True,
        help="""formio.js release/version.""")
    active = fields.Boolean(string="Active", default=True, tracking=True)
    sequence = fields.Integer()
    description = fields.Text("Description")
    is_dummy = fields.Boolean(string="Is Dummy (default version in demo data)", readonly=True)
    translation_ids = fields.One2many('formio.version.translation', 'formio_version_id', string='Translations')
    assets = fields.One2many(
        'formio.version.asset', 'version_id', string='Assets (js, css)',
        domain=[('type', '!=', 'license')])
    css_assets = fields.One2many(
        'formio.version.asset', 'version_id', domain=[('type', '=', 'css')], copy=True,
        string='CSS Assets')
    js_assets = fields.One2many(
        'formio.version.asset', 'version_id', domain=[('type', '=', 'js')], copy=True,
        string='Javascript Assets')
    license_assets = fields.One2many(
        'formio.version.asset', 'version_id',  domain=[('type', '=', 'license')], copy=True,
        string='License Assets')

    def unlink(self):
        self.assets.unlink()
        domain = [('formio_version_id', 'in', self.ids)]
        self.env['formio.version.github.tag'].search(domain).write({'state': 'available'})
        return super(Version, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Version, self).create(vals_list)
        self._update_versions_sequence()
        if res.filtered(lambda r: not r.is_dummy):
            self._archive_dummy_version()
        return res

    def write(self, vals):
        res = super(Version, self).write(vals)
        if 'name' in vals:
            self._update_versions_sequence()
        return res

    def action_add_base_translations(self):
        """ Actually this should be re-implemented to a wizard.
        The wizard should provide a list of all (base) translations to import. """

        domain = [('lang_id.active', '=', True)]
        base_translations = self.env['formio.translation'].search(domain)
        vals_list = []
        for rec in self:
            if rec.translation_ids:
                sequence = max(rec.translation_ids.mapped('sequence'))
            else:
                sequence = 1
            for trans in base_translations:
                if not rec.translation_ids.filtered(lambda t: t.base_translation_id.id == trans.id):
                    sequence += 1
                    vals = {
                        'sequence': sequence,
                        'formio_version_id': rec.id,
                        'base_translation_id': trans.id,
                        'lang_id': trans.lang_id.id,
                        'source_property': trans.source_id.property,
                        'source_text': trans.source_id.source,
                        'value': trans.value,
                    }
                    vals_list.append(vals)
        if vals_list:
            self.env['formio.version.translation'].create(vals_list)

    def action_unlink_base_translations(self):
        for rec in self:
            rec.translation_ids.filtered('base_translation_id').unlink()

    @api.model
    def _update_versions_sequence(self):
        versions = self.search([])
        names = sorted(versions.mapped('name'))
        seq = 0
        for name in names:
            seq += 1
            version = versions.filtered(lambda r: r.name == name)[0]
            version.sequence = seq

    @api.model
    def _archive_dummy_version(self):
        domain = [('is_dummy', '=', True)]
        dummy = self.search(domain)
        if dummy:
            dummy.write({'active': False})
