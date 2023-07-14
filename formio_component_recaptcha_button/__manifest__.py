# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms | reCAPTCHA Component',
    'summary': 'Drag & drop a reCAPTCHA component with (server)verification on a Form.',
    'version': '15.0.1.1',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo15.novacode.nl',
    'category': 'Forms/Forms',
    'depends': [
        'google_recaptcha',
        'formio',
    ],
    'data': [
        'views/formio_builder_views.xml',
        'views/formio_builder_templates.xml',
        'views/formio_form_public_templates.xml',
    ],
    'application': True,
    'installable': True,
    'images': [
        'static/description/banner.gif',
    ],
}
