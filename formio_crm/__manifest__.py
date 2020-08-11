# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io CRM Lead',
    'summary': 'Form.io webforms on CRM Leads',
    'version': '0.2',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'CRM',
    'depends': ['crm', 'formio'],
    'data': [
        'data/formio_crm_data.xml',
        'views/crm_lead_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Form.io - CRM Lead
==================

Build and publish (Form.io) forms for Leads.
"""
}
