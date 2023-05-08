# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Partner',
    'summary': 'Forms integration with Partners e.g. contacts, clients, customers, suppliers',
    'version': '1.2',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': ['contacts', 'formio'],
    'data': [
        'data/formio_partner_data.xml',
        'views/formio_form_views.xml',
        'views/res_partner_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': """
Forms | Partners
================

"""
}
