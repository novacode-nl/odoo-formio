# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    cr.execute("""
        UPDATE formio_builder
        SET wizard_on_change_page_save_draft = True
        WHERE wizard_on_next_page_save_draft = True
    """)

    res = env['formio.extra.asset'].search([])
    for rec in res:
        if rec.attachment_id and not rec.attachment_id.res_id:
            vals = {'res_id': rec.id}
            rec.attachment_id.write(vals)
