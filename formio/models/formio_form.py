# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import re
import requests
import uuid

from odoo import api, fields, models, _
from odoo.exceptions import AccessError

STATE_PENDING = 'PENDING'
STATE_DRAFT = 'DRAFT'
STATE_COMPLETE = 'COMPLETE'
STATE_CANCEL = 'CANCEL'


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
    state = fields.Selection(
        [(STATE_PENDING, 'Pending'), (STATE_DRAFT, 'Draft'),
         (STATE_COMPLETE, 'Completed'), (STATE_CANCEL, 'Canceled')],
        string="State", default=STATE_PENDING, track_visibility='onchange', index=True)
    url = fields.Char(compute='_compute_url', readonly=True)
    act_window_url = fields.Char(compute='_compute_act_window_url', readonly=True)
    res_model_id = fields.Many2one(related='builder_id.res_model_id', readonly=True, string='Resource Model')
    res_model_name = fields.Char(related='res_model_id.name', readonly=True, string='Resource Name')
    res_id = fields.Integer("Record ID", ondelete='restrict',
        help="Database ID of the record in res_model to which this applies")
    res_act_window_url = fields.Char(compute='_compute_res_fields', readonly=True)
    res_name = fields.Char(compute='_compute_res_fields', readonly=True)
    res_info = fields.Char(compute='_compute_res_fields', readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Assigned user',
        index=True, track_visibility='onchange')
    invitation_mail_template_id = fields.Many2one(
        'mail.template', 'Invitation Mail',
        domain=[('model', '=', 'formio.form')],
        help="This e-mail template will be sent on user assignment. Leave empty to send nothing.")
    submission_data = fields.Text('Data', default=False, readonly=True)
    submission_user_id = fields.Many2one(
        'res.users', string='Submission User', readonly=True,
        help='User who submitted the form.')
    submission_date = fields.Datetime(
        string='Submission Date', readonly=True, track_visibility='onchange',
        help='Datetime when the form was last submitted.')
    portal = fields.Boolean("Portal usage", related='builder_id.portal', help="Form is accessible by assigned portal user")
    allow_unlink = fields.Boolean("Allow delete", compute='_compute_access')

    def _compute_access(self):
        for r in self:
            unlink_form = self.get_form(r.uuid, 'unlink')
            if unlink_form:
                r.allow_unlink = True
            else:
                r.allow_unlink = False

    @api.multi
    def write(self, vals):
        if 'submission_data' in vals and self.state in [STATE_COMPLETE, STATE_CANCEL]:
            # Throw and catch exception (FormioFormException), e.g. to redirect in controller.
            return False
        res = super(Form, self).write(vals)
        return res

    @api.multi
    def action_draft(self):
        self.ensure_one()
        self.write({'state': STATE_DRAFT})

    @api.multi
    def action_complete(self):
        self.ensure_one()
        self.write({'state': STATE_COMPLETE})

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        self.write({'state': STATE_CANCEL})

    @api.multi
    def action_send_invitation_mail(self):
        self.ensure_one()

        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        if self.portal:
            template_id = self.env.ref('formio.mail_invitation_portal_user').id
        else:
            template_id = self.env.ref('formio.mail_invitation_internal_user').id
        ctx = dict(
            default_composition_mode='comment',
            default_res_id=self.id,
            default_model='formio.form',
            default_use_template=bool(template_id),
            default_template_id=template_id,
            custom_layout='mail.mail_notification_light'
        )
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def _default_uuid(self):
        return str(uuid.uuid4())

    @api.onchange('builder_id')
    def _onchange_builder(self):
        if not self.env.user.has_group('formio.group_formio_user_all_forms'):
            self.user_id = self.env.user.id

    @api.onchange('portal')
    def _onchange_portal(self):
        res = {}
        group_portal = self.env.ref('base.group_portal').id
        group_formio_user = self.env.ref('formio.group_formio_user').id
        group_formio_user_all = self.env.ref('formio.group_formio_user_all_forms').id
        if not self.portal:
            if self.user_id.has_group('base.group_portal'):
                self.user_id = False
            res['domain'] = {
                'user_id': [
                    ('groups_id', '!=', group_portal),
                    '|',
                    ('groups_id', '=', group_formio_user),
                    ('groups_id', '=', group_formio_user_all),
                ]}
        else:
            res['domain'] = {
                'user_id': [
                    '|',
                    ('groups_id', '=', group_portal),
                    ('groups_id', '!=', False)
                ]
            }
        return res

    def _compute_url(self):
        # sudo() is needed for regular users.
        for r in self:
            url = '{base_url}/formio/form/{uuid}'.format(
                base_url=r.env['ir.config_parameter'].sudo().get_param('web.base.url'),
                uuid=r.uuid)
            r.url = url

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
            'url': self.url,
            'target': 'self',
        }

    @api.multi
    def action_open_res_act_window(self):
        raise NotImplementedError

    @api.model
    def get_form(self, uuid, mode):
        """ Verifies access to form and return form or False (if no access). """

        if not self.env['formio.form'].check_access_rights(mode, False):
            return False

        form = self.search([('uuid', '=', uuid)], limit=1)
        if form:
            try:
                # Catch the deny access exception
                form.check_access_rule(mode)
            except AccessError as e:
                return False
        elif self.env.user.has_group('base.group_portal'):
            form = self.sudo().search([('uuid', '=', uuid)], limit=1)
            if not form or form.builder_id.portal is False or form.user_id.id != self.env.user.id:
                return False
        return form


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def check(self, mode, values=None):
        to_check = self
        if self.ids:
            self._cr.execute("SELECT id FROM ir_attachment WHERE res_model = 'formio.version.asset' AND id IN %s", [tuple(self.ids)])
            asset_ids = [r[0] for r in self._cr.fetchall()]
            if asset_ids:
                to_check = self - self.browse(asset_ids)
        super(IrAttachment, to_check).check(mode, values)
