# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class TranslationSource(models.Model):
    _name = 'formio.translation.source'
    _description = 'Formio Version Translation Source'
    _rec_name = 'source'

    property = fields.Text(string='Property', required=True)
    source = fields.Text(string='Source', required=True)

    @api.multi
    @api.depends('property', 'source')
    def name_get(self):
        res = []
        for r in self:
            name = '[{property}]: {source}'.format(
                property=r.property, source=r.source
            )
            res.append((r.id, name))
        return res
