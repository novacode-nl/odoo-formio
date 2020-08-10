# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Website',
    'summary': 'Form Snippet, Other website integration',
    'version': '1.1',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['formio', 'website'],
    'data': [
        'data/website_data.xml',
        'data/website_formio_demo_data.xml',
        'views/formio_builder_views.xml',
        'views/website_formio_templates.xml',
        'views/website_formio_snippets.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
}
