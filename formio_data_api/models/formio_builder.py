# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from formiodata.builder import Builder
from odoo import fields, models, api, tools, _

_logger = logging.getLogger(__name__)


class FormioBuilder(models.Model):
    _inherit = 'formio.builder'

    def __getattr__(self, name):
        if name == '_formio' and self._name == 'formio.builder':
            if self.schema is False:
                # HACK masquerade empty Builder object
                builder_obj = Builder('{}')
            else:
                builder_obj = Builder(self.schema)
            return builder_obj
        else:
            return self.__getattribute__(name)

    @api.multi
    def write(self, vals):
        super(FormioBuilder, self).write(vals)
        self.env['formio.component'].synchronize_components(self.ids)
