# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import re
import uuid

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IrAttachment(models.AbstractModel):
    _inherit = 'ir.attachment'

    # Here for all kinds of integration e.g. file component, reporting
    formio_form_id = fields.Many2one(
        'formio.form', string='formio.form', compute='_compute_formio_form_id', store=True, default=False, index=True)
    formio_asset_formio_version_id = fields.Many2one(
        'formio.version', string='formio.js version',
        help='Mostly files from the formio.js project - https://github.com/formio/formio.js')
    formio_ref = fields.Char(
        string="Forms Ref",
        help="Identifies an attachment with a related Forms/Builder record.",
    )

    @api.constrains('formio_ref')
    def constaint_check_formio_ref(self):
        for rec in self:
            if rec.formio_ref:
                if re.search(r"[^a-zA-Z0-9_-]", rec.formio_ref) is not None:
                    raise ValidationError(_('Forms Ref is invalid. Use ASCII letters, digits, "-" or "_".'))

    @api.model_create_multi
    def create(self, vals_list):
        models = self._formio_ref_models()
        for vals in vals_list:
            generate_formio_ref = False
            if not vals.get('formio_ref'):
                if vals.get('res_model') in models:
                    generate_formio_ref = True
                elif self._context.get('default_res_model') in models:
                    generate_formio_ref = True
            if generate_formio_ref:
                vals['formio_ref'] = str(uuid.uuid4())
        return super(IrAttachment, self).create(vals_list)

    def write(self, vals):
        models = self._formio_ref_models()
        if vals.get('res_model') in models and not vals.get('formio_ref'):
            vals['formio_ref'] = str(uuid.uuid4())
        return super(IrAttachment, self).write(vals)

    @api.depends('res_model')
    def _compute_formio_form_id(self):
        for attach in self:
            if attach.res_model == 'formio.form' and attach.res_id:
                # XXX optimize with 1 browse(ids) query and write on records?
                form = self.env['formio.form'].browse(attach.res_id)
                attach.formio_form_id = form.id

    @api.model
    def check(self, mode, values=None):
        to_check = self
        if self.ids:
            self._cr.execute(
                """
                SELECT
                    id
                FROM
                    ir_attachment
                WHERE
                    res_model IN ('formio.version.asset')
                    AND id IN %s""",
                [tuple(self.ids)],
            )
            asset_ids = [r[0] for r in self._cr.fetchall()]
            if asset_ids:
                to_check = self - self.browse(asset_ids)
        super(IrAttachment, to_check).check(mode, values)

    def copy(self, default=None):
        self.ensure_one()
        if self.formio_ref:
            default = dict(default or {})
            default['formio_ref'] = str(uuid.uuid4())
        return super().copy(default)

    def _formio_ref_models(self):
        return ['formio.version.asset']
