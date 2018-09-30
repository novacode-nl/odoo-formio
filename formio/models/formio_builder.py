# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import requests

from odoo import api, fields, models, _


class Builder(models.Model):

    _name = 'formio.builder'
    _description = 'Formio Builder'

    name = fields.Char(required=True)
    schema = fields.Text()
    edit_url = fields.Char(compute='_compute_edit_url', readonly=True)

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
