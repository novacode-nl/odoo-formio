# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, registry, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    res = env['formio.extra.asset'].search([])
    for rec in res:
        if rec.attachment_id and not rec.attachment_id.res_id:
            vals = {'res_id': rec.id}
            rec.attachment_id.write(vals)
