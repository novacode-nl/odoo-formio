# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | CRM',
    'summary': 'Forms integration with CRM Leads',
    'version': '2.0',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': ['crm', 'formio'],
    'data': [
        'data/formio_crm_data.xml',
        'views/crm_lead_views.xml',
        'views/formio_form_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': """
Forms | CRM
===========

"""
}
