# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    formio_builder = env['formio.builder']
    domain = [('portal', '=', True)]
    for builder in formio_builder.search(domain):
        builder.write({'portal_direct_create': True})
