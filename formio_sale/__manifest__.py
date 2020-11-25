# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms Sales',
    'summary': 'Formio webforms on Sale Orders/Quotes',
    'version': '0.4',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Sales',
    'depends': ['sale_management', 'formio', 'formio_data_api'],
    'data': [
        'data/formio_sale_data.xml',
        'data/formio_demo_data.xml',
        'views/sale_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Forms - Sales
=============

Build and publish (Formio) forms for Sale Orders/Quotes.
"""
}
