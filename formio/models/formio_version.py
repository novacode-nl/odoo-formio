# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from pkg_resources import parse_version

from odoo import api, fields, models


class Version(models.Model):
    _name = 'formio.version'
    _description = 'Formio Version'
    _order = 'sequence DESC'

    name = fields.Char(
        "Name", required=True, track_visibility='onchange',
        help="""Form.io release/version.""")
    sequence = fields.Integer()
    description = fields.Text("Description")
    translations = fields.Many2many('formio.translation', string='Translations')
    assets = fields.One2many('formio.version.asset', 'version_id', string='Assets')
    css_assets = fields.One2many(
        'formio.version.asset', 'version_id', domain=[('type', '=', 'css')],
        string='CSS Assets')
    js_assets = fields.One2many(
        'formio.version.asset', 'version_id', domain=[('type', '=', 'js')],
        string='Javascript Assets')

    def unlink(self):
        domain = [('formio_version_id', '=', self.ids)]
        self.env['formio.version.github.tag'].search(domain).write({'state': 'available'})
        return super(Version, self).unlink()

    @api.model
    def create(self, vals):
        res = super(Version, self).create(vals)
        self._update_versions_sequence()
        return res

    def write(self, vals):
        res = super(Version, self).write(vals)
        if 'name' in vals:
            self._update_versions_sequence()
        return res

    @api.model
    def _update_versions_sequence(self):
        versions = self.search([])
        names = versions.mapped('name')
        names = sorted(names, key=parse_version)
        seq = 0
        for name in names:
            seq += 1
            version = versions.filtered(lambda r: r.name == name)[0]
            version.sequence = seq
        
