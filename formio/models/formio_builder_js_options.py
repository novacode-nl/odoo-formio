# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class BuilderJsOptionsTemplate(models.Model):
    _name = 'formio.builder.js.options.template'
    _description = 'Formio Builder JavaScript Options Template'
    _order = 'name ASC'

    name = fields.Char(string="Name", required=True)
    value = fields.Text(string="Value (JSON)")
