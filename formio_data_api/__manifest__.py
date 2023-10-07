# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Data API',
    'summary': 'Python API for Form Builder and Form/Submission data',
    'version': '16.0.2.2',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo16.novacode.nl',
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
        'static/description/banner.gif',
    ],
    'description': 'Python API for Forms data (builder, form/submission)',
}
