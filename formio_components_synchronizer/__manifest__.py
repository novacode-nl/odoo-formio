# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms • Components Synchronizer',
    'summary': 'Saves Form Components as database records.',
    'version': '17.0',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo17.novaforms.app',
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
        'static/description/banner.png',
    ],
    'description': 'Saves Form Components as database records.'
}
