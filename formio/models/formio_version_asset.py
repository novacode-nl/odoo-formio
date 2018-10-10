# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models, _


class VersionAsset(models.Model):
    _name = 'formio.version.asset'
    _description = 'Formio Version Asset'

    version_id = fields.Many2one('formio.version', string='Version')
    type = fields.Selection([('js', 'js'), ('css', 'css')], string='Type')
    attachment_id = fields.Many2one('ir.attachment', string="Attachment", required=True, ondelete='cascade')
    attachment_type = fields.Selection(related='attachment_id.type', string='Attachment Type', readonly=True)
    sequence = fields.Integer(string='Sequence', default=1)
