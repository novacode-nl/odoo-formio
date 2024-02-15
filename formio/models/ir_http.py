# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import models
from odoo.http import request

from ..controllers.utils import BadCSRF


class IrHttp(models.AbstractModel):
    _inherit = ['ir.http']

    @classmethod
    def _get_error_html(cls, env, code, values):
        """ In case of BadCSRF (failed validate_csrf() method):
        Hide the traceback from other users, to secure the (server)
        internals.
        """
        if isinstance(values['exception'], BadCSRF):
            if (
                not request.env.user.has_group('formio.group_formio_admin')
                and not request.env.user.has_group('base.group_system')
            ):
                # Hide traceback from other users, to secure the (server) internals
                del values['traceback']
            values['error_message'] = values['exception'].description
            return code, env['ir.ui.view']._render_template('http_routing.%s' % code, values)
        else:
            return super(IrHttp, cls)._get_error_html(env, code, values)
