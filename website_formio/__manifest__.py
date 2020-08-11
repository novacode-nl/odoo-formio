# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Website',
    'summary': 'Website integration (redirect to website page or URL after form submission)',
    'version': '1.0',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['formio', 'website'],
    'data': [
        'data/website_data.xml',
        'views/formio_builder_views.xml',
        # TODO FIX snippet (backport this v13 implementation)
        # 'data/website_formio_demo_data.xml',
        # 'views/website_formio_templates.xml',
        # 'views/website_formio_snippets.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
}
