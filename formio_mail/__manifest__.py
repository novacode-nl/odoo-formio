# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Mail',
    'summary': 'Send Forms via mail',
    'version': '0.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    # 'live_test_url': 'https://demo17.novaforms.app',
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
    'description': "Send forms via mail after completion."
}
