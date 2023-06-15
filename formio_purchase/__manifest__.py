# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Purchase',
    'summary': 'Forms integration with Purchase Orders',
    'version': '2.0',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': ['purchase', 'formio', 'formio_data_api'],
    'data': [
        'data/formio_purchase_data.xml',
        'data/formio_demo_data.xml',
        'views/formio_form.xml',
        'views/purchase_order.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': ''
}
