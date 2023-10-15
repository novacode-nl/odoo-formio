# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from . import models
from . import controllers
from . import utils
from . import wizard

import odoo
from odoo import api, SUPERUSER_ID
from functools import partial

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    VersionGitHubTag = env['formio.version.github.tag']
    try:
        VersionGitHubTag.check_and_register_available_versions()
    except Exception as e:
        msg_lines = [
            'Could not immediately check and register new formio.js GitHub releases (tags).',
            'Error: %s' % e,
            'Suggestion: Check the network connection.'
        ]
        _logger.warning('\n'.join(msg_lines))
    try:
        Param = env['ir.config_parameter'].sudo()
        param_version = Param.get_param('formio.default_version')
        if param_version:
            version_name = 'v%s' % param_version
            domain = [('name', '=', version_name)]
            version_github_tag = VersionGitHubTag.search(domain, limit=1)
            if version_github_tag and len(version_github_tag) == 1:
                version_github_tag.action_download_install()
    except Exception as e:
        msg_lines = [
            'Could not immediately download and install formio.js version %s.' % version_name,
            'Error: %s' % e,
            'Suggestion: Check the network connection.'
        ]
        _logger.warning('\n'.join(msg_lines))


def uninstall_hook(env):
    def delete_config_parameter(dbname):
        db_registry = odoo.modules.registry.Registry.new(dbname)
        with api.Environment.manage(), db_registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            env['ir.config_parameter'].search(
                [('key', '=', 'formio.default_builder_js_options_id')]).unlink()
    # cr.postcommit.add(partial(delete_config_parameter, cr.dbname))
