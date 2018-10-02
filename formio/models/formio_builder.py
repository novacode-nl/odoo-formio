# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import re
import requests

from odoo import api, fields, models, _


class Builder(models.Model):
    _name = 'formio.builder'
    _description = 'Formio Builder'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        "Name", required=True, track_visibility='onchange',
        help="""Identifies this specific form.\n
        This name can be used in APIs. Use only ASCII letters, digits, "-" or "_".
        """)
    title = fields.Char("Title",
        help="Form title in the current language", track_visibility='onchange',
        default="Untitled Form")
    description = fields.Text("Description")
    res_model_id = fields.Many2one(
        "ir.model",
        "Resource Model",
        ondelete='restrict', track_visibility='onchange',
        help="Model as resource this form represents or acts on")
    schema = fields.Text()
    edit_url = fields.Char(compute='_compute_edit_url', readonly=True)
    forms = fields.One2many('formio.form', 'builder_id', string='Forms')

    @api.constrains('name')
    def constaint_check_name(self):
        self.ensure_one
        if re.search(r"[^a-zA-Z0-9_-]", self.name) is not None:
            raise ValidationError('Name is invalid. Use ASCII letters, digits, "-" or "_".')

    def _compute_edit_url(self):
        url = '{base_url}/formio/builder/{builder_id}'.format(
            base_url=self.env['ir.config_parameter'].get_param('web.base.url'),
            builder_id=self.id)
        self.edit_url = url
        
    @api.multi
    def action_edit(self):
        # url = '{base_url}/formio/builder/{builder_id}'.format(
        #     base_url=self.env['ir.config_parameter'].get_param('web.base.url'),
        #     builder_id=self.id)

        return {
            'type': 'ir.actions.act_url',
            'url': self.edit_url,
            'target': 'new',
        }
