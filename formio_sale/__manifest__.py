# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Sales',
    'summary': 'Form.io webforms on Sale Orders/Quotes',
    'version': '0.4',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
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
Form.io - Sales
===============

Build and publish (Form.io) forms for Sale Orders/Quotes.
"""
}
