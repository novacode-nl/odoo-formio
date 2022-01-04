# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Mail',
    'summary': 'Send Forms via mail',
    'version': '0.2',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Extra Tools',
    'depends': ['contacts', 'mail', 'formio_report_qweb', 'formio_component'],
    'data': [
        'security/ir.model.access.csv',
        'views/formio_builder_views.xml',
        'views/formio_mail_recipient_views.xml',
        'views/formio_menu.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': """
Forms | Mail
==================

Send forms via mail after completion.
"""
}
