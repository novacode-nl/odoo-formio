# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class Version(models.Model):
    _name = 'formio.version'
    _description = 'Formio Version'

    name = fields.Char(
        "Name", required=True, track_visibility='onchange',
        help="""Form.io release/version.""")
    description = fields.Text("Description")
    assets = fields.One2many('formio.version.asset', 'version_id', string='Assets')
