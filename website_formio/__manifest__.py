# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | Website (integration)',
    'summary': 'Website integration, redirect page',
    'version': '1.4',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo14.novacode.nl',
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
        'static/description/banner.gif',
    ],
}
