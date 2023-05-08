# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Mail',
    'summary': 'Send Forms via mail',
    'version': '0.2',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    # 'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': [
        'mail',
        'formio_components_synchronizer',
        'formio_report_qweb'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/formio_builder_views.xml',
        'views/formio_mail_recipient_address_views.xml',
        'views/formio_menu.xml',
    ],
    'application': True,
    'installable': False,
    'images': [
        'static/description/banner.gif',
    ],
    'description': """
Forms | Mail
============

Send forms via mail after completion.
"""
}
