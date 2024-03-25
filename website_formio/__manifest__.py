# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms • Website Integration',
    'summary': "Redirect a form (portal, website) to a configurable website page.",
    'version': '17.0.1.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novaforms.app',
    'live_test_url': 'https://demo17.novaforms.app',
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
    ],
    'demo': [
        'data/website_formio_demo_data.xml'
    ],
    'assets': {
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
