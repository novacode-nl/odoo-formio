# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Website (Snippet etc)',
    'summary': 'Forms Snippet, Other website integration',
    'version': '1.7',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Extra Tools',
    'depends': ['formio', 'website', 'website_editor_unsanitize_html_field'],
    'data': [
        'data/website_data.xml',
        'data/website_formio_demo_data.xml',
        'views/formio_builder_views.xml',
        'views/website_formio_templates.xml',
        'views/website_formio_snippets.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.gif',
    ],
}
