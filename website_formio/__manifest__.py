# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Website',
    'summary': 'Redirect to website-page or URL - after form submission.',
    'version': '1.0',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['formio', 'website'],
    'data': [
        'data/website_data.xml',
        'views/formio_builder_views.xml',
    ],
    'application': False,
    'images': [
        'static/description/banner.gif',
    ],
}
