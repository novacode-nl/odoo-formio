# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import re
import requests
import uuid

from odoo import api, fields, models, _


class Form(models.Model):
    _name = 'formio.form'
    _description = 'Formio Form'
    _inherit = ['mail.thread']

    _rec_name = 'name'

    builder_id = fields.Many2one(
        'formio.builder', string='Form builder', ondelete='restrict', store=True)
    name = fields.Char(related='builder_id.name', readonly=True)
    uuid = fields.Char(
        default=lambda self: self._default_uuid(), required=True, readonly=True, copy=False,
        string='UUID')
    title = fields.Char(related='builder_id.title', readonly=True)
    edit_url = fields.Char(compute='_compute_edit_url', readonly=True)
    act_window_url = fields.Char(compute='_compute_act_window_url', readonly=True)
    res_model_id = fields.Many2one(related='builder_id.res_model_id', readonly=True, string='Resource Model')
    res_model_name = fields.Char(related='res_model_id.name', readonly=True, string='Resource Name')
    res_id = fields.Integer("Record ID", ondelete='restrict',
        help="Database ID of the record in res_model to which this applies")
    res_act_window_url = fields.Char(compute='_compute_res_fields', readonly=True)
    res_name = fields.Char(compute='_compute_res_fields', readonly=True)
    res_info = fields.Char(compute='_compute_res_fields', readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Assigned to', default=lambda self: self.env.uid,
        index=True, track_visibility='onchange')
    submission_data = fields.Text('Data', default=False, readonly=True)
    submission_user_id = fields.Many2one(
        'res.users', string='Submission User', readonly=True,
        help='User who submitted the form.')
    submission_date = fields.Datetime(
        string='Submission Date', readonly=True, track_visibility='onchange',
        help='Datetime when the form was last submitted.')

    @api.model
    def _default_uuid(self):
        return str(uuid.uuid4())
    
    def _compute_edit_url(self):
        # sudo() is needed for regular users.
        for r in self:
            url = '{base_url}/formio/form/{uuid}'.format(
                base_url=r.env['ir.config_parameter'].sudo().get_param('web.base.url'),
                uuid=r.uuid)
            r.edit_url = url

    def _compute_act_window_url(self):
        # sudo() is needed for regular users.
        for r in self:
            action = self.env.ref('formio.action_formio_form')
            url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                id=r.id,
                model=r._name,
                action=action.id)
            r.act_window_url = url

    def _compute_res_fields(self):
        for r in self:
            r.res_act_window_url = False
            r.res_name = False
            r.res_info = False
        
    @api.multi
    def action_formio(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.edit_url,
            'target': 'new',
        }

    @api.multi
    def action_open_res_act_window(self):
        raise NotImplementedError
