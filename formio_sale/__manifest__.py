# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Sales',
    'summary': 'Forms integration with Sale Orders/Quotations',
    'version': '1.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': ['sale_management', 'formio', 'formio_data_api'],
    'data': [
        'data/formio_sale_data.xml',
        'data/formio_demo_data.xml',
        'views/formio_form_views.xml',
        'views/sale_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': """
Forms | Sales
=============

"""
}
