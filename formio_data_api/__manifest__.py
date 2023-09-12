# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Data API',
    'summary': 'Python API for Form Builder and Form/Submission data',
    'version': '15.0.3.3',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': ['formio', 'mail'],
    'data': [
        'security/ir_model_access.xml',
        'views/formio_builder_views.xml',
        'views/formio_component_server_api_views.xml'
    ],
    'external_dependencies': {
        'python': ['formio-data'],
    },
    'application': True,
    'installable': True,
    'images': [
        'static/description/banner.gif',
    ]
}
