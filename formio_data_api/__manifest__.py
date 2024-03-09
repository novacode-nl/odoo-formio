# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms • Data API',
    'summary': 'Python API for Form Builder and Form/Submission data',
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo17.novaforms.app',
    'category': 'Forms/Forms',
    'depends': [
        'formio',
        'mail'
    ],
    'data': [],
    'external_dependencies': {
        'python': ['formio-data'],
    },
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': 'Python API for Forms data (builder, form/submission)',
}
