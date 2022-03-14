# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Storage Filestore',
    'summary': 'Store uploads/files by URL in Odoo filestore (attachments)',
    'version': '0.10',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Extra Tools',
    'depends': ['formio', 'formio_data_api'],
    'data': [
        'data/formio_storage_filestore_data.xml',
        'data/ir_cron_data.xml'
    ],
    'installable': True,
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': ''
}
