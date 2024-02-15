# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Purchase',
    'summary': 'Forms integration with Purchase Orders',
    'version': '0.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo17.novaforms.app',
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
