# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Mail',
    'summary': 'Form.io Send webforms via mail',
    'version': '0.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Extra Tools',
    'depends': ['contacts', 'formio_report_qweb'],
    'data': [
        'views/formio_builder_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Form.io - Mail
==================

Send forms via mail after completion.
"""
}
