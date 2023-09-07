# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Components Synchronizer',
    'summary': 'Saves Form Components as database records.',
    'version': '15.0.1.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Forms/Forms',
    'depends': ['formio', 'formio_data_api'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_server_action.xml',
        'views/formio_component_views.xml',
        'views/formio_builder_views.xml',
        'views/formio_menu.xml',
    ],
    'application': True,
    'installable': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': """
"""
}
