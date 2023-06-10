# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | File Storage',
    'summary': 'Store uploaded files by URL in the filestore (attachments)',
    'version': '1.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo14.novacode.nl',
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
