# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Website Editor: Unsanitize HTML Field',
    'summary': 'Upon saving record (from website editor) unsanitize HTML Field, if configured for certain Model and Field.',
    'version': '0.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Extra Tools',
    'depends': ['website'],
    'data': [
        'security/ir_model_access.xml',
        'data/website_editor_unsanitize_html_field_data.xml',
        'views/website_editor_unsanitize_html_field_views.xml',
    ],
    'application': False,
    'images': [
        'static/description/banner.gif',
    ],
}
