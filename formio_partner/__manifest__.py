# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Partner',
    'summary': 'Form.io webforms on Partners',
    'version': '0.2',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Contacts',
    'depends': ['contacts', 'formio'],
    'data': [
        'data/formio_partner_data.xml',
        'views/formio_form_views.xml',
        'views/res_partner_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Form.io - Partners
==================

Build and publish (Form.io) forms for Partners.
"""
}
