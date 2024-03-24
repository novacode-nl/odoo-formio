# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging
import uuid

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    builders_name = {}
    builders = env['formio.builder'].search([])
    for rec in builders:
        if rec.name not in builders_name:
            builders_name[rec.name] = rec
        else:
            builders_name[rec.name] |= rec
    for name, builders in builders_name.items():
        _logger.info(
            'Updating formio.builder %s records field public_uuid ...' % name
        )
        builders.write({'public_uuid': str(uuid.uuid4())})
