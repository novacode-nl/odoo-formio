# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class Builder(models.Model):
    _inherit = 'formio.builder'

    submit_done_page = fields.Many2one('website.page', domain=[('is_published', '=', True), ('url', '!=', '/')])
