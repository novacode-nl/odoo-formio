# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms • File Storage',
    'summary': 'Store uploaded files by URL in the filestore (attachments)',
    'version': '0.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo17.novaforms.app',
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
        'static/description/banner.png',
    ],
    'description': ''
}
