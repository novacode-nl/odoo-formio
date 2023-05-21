# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    domain = [('translations', '!=', False)]
    versions = env['formio.version'].search(domain)
    versions.action_add_base_translations()
