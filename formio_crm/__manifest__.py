# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms • CRM',
    'summary': 'Forms integration with CRM Leads',
    'version': '0.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo17.novaforms.app',
    'category': 'Forms/Forms',
    'depends': [
        'crm',
        'formio'
    ],
    'data': [
        'data/formio_crm_data.xml',
        'views/crm_lead_views.xml',
        'views/formio_form_views.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': 'Forms integration with CRM Leads',
}
