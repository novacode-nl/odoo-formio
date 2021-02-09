# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Data API',
    'summary': 'Python API for Forms data (builder, form/submission).',
    'version': '0.5',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['formio'],
    'data': [
        'views/formio_component_views.xml',
        'views/formio_menu.xml',
    ],
    'external_dependencies': {
        'python': ['formio-data'],
    },
    'application': False,
    'images': [
        'static/description/banner.gif',
    ],
    'description': """
Forms | Data API
================

"""
}
