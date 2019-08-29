# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import re
import requests

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Builder(models.Model):
    _name = 'formio.builder'
    _description = 'Formio Builder'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'

    name = fields.Char(
        "Name", required=True, track_visibility='onchange',
        help="""Identifies this specific form. This name can be used in APIs. \
        Use only ASCII letters, digits, "-" or "_".""")
    title = fields.Char(
        "Title", required=True, default="Untitled Form",
        help="The form title in the current language", track_visibility='onchange')
    description = fields.Text("Description")
    formio_version_id = fields.Many2one(
        'formio.version', string='Form.io Version', required=True,
        track_visibility='onchange',
        help="""Loads the specific Form.io Javascript API/libraries version (sourcecode: \https://github.com/formio/formio.js)""")
    formio_css_assets = fields.One2many(related='formio_version_id.css_assets', string='Form.io CSS')
    formio_js_assets = fields.One2many(related='formio_version_id.js_assets', string='Form.io Javascript')
    res_model_id = fields.Many2one(
        "ir.model",
        "Resource Model",
        ondelete='restrict', track_visibility='onchange',
        help="Model as resource this form represents or acts on")
    schema = fields.Text()
    edit_url = fields.Char(compute='_compute_edit_url', readonly=True)
    act_window_url = fields.Char(compute='_compute_act_window_url', readonly=True)
    forms = fields.One2many('formio.form', 'builder_id', string='Forms')
    portal = fields.Boolean("Portal usage", track_visibility='onchange', help="Form is accessible by assigned portal user")
    view_as_html = fields.Boolean("View as HTML", track_visibility='onchange', help="View submission as a HTML view instead of disabled webform.")

    @api.constrains('name')
    def constaint_check_name(self):
        self.ensure_one
        if re.search(r"[^a-zA-Z0-9_-]", self.name) is not None:
            raise ValidationError('Name is invalid. Use ASCII letters, digits, "-" or "_".')

    def _compute_edit_url(self):
        # sudo() is needed for regular users.
        url = '{base_url}/formio/builder/{builder_id}'.format(
            base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            builder_id=self.id)
        self.edit_url = url

    def _compute_act_window_url(self):
        # sudo() is needed for regular users.
        action = self.env.ref('formio.action_formio_builder')
        url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
            id=self.id,
            model=self._name,
            action=action.id)
        self.act_window_url = url
        
    @api.multi
    def action_edit(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.edit_url,
            'target': 'self',
        }
