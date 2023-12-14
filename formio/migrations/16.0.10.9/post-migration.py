# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # new/updated to: default_asset_css_bootstrap_4_4_1
    env.ref('formio.default_asset_css_bootstrap_4_1_3').unlink()
