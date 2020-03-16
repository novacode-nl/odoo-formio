# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Partner',
    'summary': 'Form.io webforms on Partners',
    'version': '0.1',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
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
===============

Build and publish (Form.io) forms for Partners.
"""
}
