# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Filestore Storage',
    'summary': 'Store uploads/files by URL in Odoo filestore (attachments)',
    'version': '16.0.2.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo16.novacode.nl',
    'category': 'Forms/Forms',
    'depends': [
        'formio',
        'formio_data_api'
    ],
    'data': [
        'data/formio_storage_filestore_data.xml',
        'data/ir_cron_data.xml'
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
    'description': ''
}
