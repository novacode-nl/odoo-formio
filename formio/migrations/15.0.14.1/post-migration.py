# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
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
            domain = [('name', '=', version_name), ('state', '!=', 'installed')]
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
