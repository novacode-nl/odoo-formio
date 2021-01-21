# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from formiodata.builder import Builder
from odoo import fields, models, api, tools, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Builder(models.Model):
    _inherit = 'formio.builder'

    def __getattr__(self, name):
        if name == '_formio':
            if '_formio' not in self.__dict__:
                if self.schema is False:
                    # HACK masquerade empty Builder object
                    self._formio = Builder('{}')
                else:
                    self._formio = Builder(self.schema)
                return self._formio
        else:
            return self.__getattribute__(name)

    @api.multi
    def write(self, vals):
        super(Builder, self).write(vals)
        self.env['formio.component'].synchronize_components(self.ids)
