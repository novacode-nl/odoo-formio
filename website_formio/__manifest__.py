# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Website (Block etc)',
    'summary': "'Drag & drop' Form Block, other website integration",
    'version': '2.0',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo14.novacode.nl',
    'category': 'Extra Tools',
    'depends': ['formio', 'website', 'website_editor_unsanitize_html_field'],
    'data': [
        'data/website_data.xml',
        'data/website_formio_demo_data.xml',
        'security/ir.model.access.csv',
        'views/formio_builder_views.xml',
        'views/formio_website_page.xml',
        'views/website_formio_templates.xml',
        'views/website_formio_snippets.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
}
