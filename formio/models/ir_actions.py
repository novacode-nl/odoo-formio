# Copyright 2023 Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ServerAction(models.Model):
    _inherit = "ir.actions.server"

    formio_code = fields.Char(
        string="Forms Code", help="Identifies a server action with related form builder."
    )

    @api.constrains('formio_code')
    def constaint_checkq_formio_code(self):
        self.ensure_one
        if self.formio_code:
            if re.search(r"[^a-zA-Z0-9_-]", self.formio_code) is not None:
                raise ValidationError(_('Forms Code is invalid. Use ASCII letters, digits, "-" or "_".'))

    @api.constrains('formio_code')
    def _constraint_unique_formio_code(self):
        for rec in self:
            domain = [("formio_code", "=", rec.formio_code)]
            if self.search_count(domain) > 1:
                msg = _(
                    'A Server Action with Forms Code "%s" already exists.\nForms Code should be unique.'
                ) % (rec.formio_code)
                raise ValidationError(msg)
