# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Website (Block etc)',
    'summary': 'Form Block, other website integration',
    'version': '1.8',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo13.novacode.nl',
    'category': 'Extra Tools',
    'depends': ['formio', 'website', 'website_editor_unsanitize_html_field'],
    'installable': False,
    'application': True,
    'data': [
        'data/website_data.xml',
        'data/website_formio_demo_data.xml',
        'views/formio_builder_views.xml',
        'views/website_formio_snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'formio/static/lib/iframe-resizer/iframeResizer.min.js'
        ],
        'web.assets_editor': [
            'website_formio/static/src/js/website_formio_editor.js',
            'formio/static/src/js/formio_form_container.js'
        ],
    },
    'images': [
        'static/description/banner.gif',
    ],
}
