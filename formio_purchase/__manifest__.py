# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Purchase',
    'summary': 'Forms integration with Purchase Orders',
    'version': '16.0.1.0',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': [
        'purchase',
        'formio',
        'formio_data_api'
    ],
    'data': [
        'data/formio_purchase_data.xml',
        'views/formio_form.xml',
        'views/purchase_order.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': 'Forms integration with Purchase Orders',
}
