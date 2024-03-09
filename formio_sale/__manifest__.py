# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms • Sales',
    'summary': 'Forms integration with Sale Orders/Quotations',
    'version': '0.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo17.novaforms.app',
    'category': 'Forms/Forms',
    'depends': [
        'sale_management',
        'formio',
        'formio_data_api'
    ],
    'data': [
        'data/formio_sale_data.xml',
        'views/formio_form_views.xml',
        'views/sale_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': 'Forms integration with Sale Orders/Quotations'
}
