# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import re
import requests

from odoo import api, fields, models, _


class Form(models.Model):
    _name = 'formio.form'
    _description = 'Formio Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'name'

    builder_id = fields.Many2one(
        'formio.builder', string='Form builder', ondelete='restrict', store=True)
    name = fields.Char(related='builder_id.name', readonly=True)
    title = fields.Char(related='builder_id.title', readonly=True)
    data = fields.Text('Submission Data', default=False)
    edit_url = fields.Char(compute='_compute_edit_url', readonly=True)
    res_model_id = fields.Many2one(related='builder_id.res_model_id', readonly=True, string='Resource Model')
    res_id = fields.Integer("Record ID", ondelete='restrict',
        help="Database ID of the record in res_model to which this applies")

    def _compute_edit_url(self):
        url = '{base_url}/formio/form/{form_id}'.format(
            base_url=self.env['ir.config_parameter'].get_param('web.base.url'),
            form_id=self.id)
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
