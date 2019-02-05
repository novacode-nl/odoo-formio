# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class Translation(models.Model):
    _name = 'formio.translation'
    _description = 'Formio Version Translation'
    _order = 'lang_id ASC'

    lang_id = fields.Many2one('res.lang', string='Language', required=True)
    property = fields.Text(string='Property', required=True)
    value = fields.Text(string='Value', required=True)
    note = fields.Text(string='Note')

    @api.multi
    @api.depends('lang_id', 'property', 'value')
    def name_get(self):
        res = []

        for r in self:
            name = '{lang}: {property} => {value}'.format(
                lang=r.lang_id, property=r.property, value=r.value
            )
                
            res.append((r.id, name))

        return res
