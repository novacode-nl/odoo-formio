# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms • Website Integration',
    'summary': "'Drag & drop' Form Block, other website integration",
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo16.novacode.nl',
    'category': 'Forms/Forms',
    'depends': [
        'formio',
        'website',
    ],
    'data': [
        'data/website_data.xml',
        'security/ir.model.access.csv',
        'views/formio_builder_views.xml',
        'views/formio_website_page.xml',
        'views/website_formio_templates.xml',
        'views/website_formio_snippets.xml',
    ],
    'demo': [
        'data/website_formio_demo_data.xml'
    ],
    'assets': {
        # 'web.assets_backend': [
        #     'website_formio/static/src/js/website_formio_editor.js'
        # ],
        'web.assets_frontend': [
            'formio/static/src/js/formio_form_container.js',
        ],
        'web.assets_common': [
            'formio/static/lib/iframe-resizer/iframeResizer.min.js',
        ],
    },
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
}
