# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io',
    'summary': 'Build, deploy and store web forms with the "Form.io" Form Builder',
    'version': '2.2',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['web', 'portal', 'mail'],
    'qweb': [
        'static/src/xml/formio.xml',
    ],
    'data': [
        'data/formio_version_data.xml',
        'data/formio_version_asset_data.xml',
        'data/formio_demo_data.xml',
        'data/mail_template_data.xml',
        # translations
        'data/formio_translations_sources.xml',
        'data/formio_translations_nl.xml',
        'data/formio_translations_nl_BE.xml',
        # security
        'security/formio_security.xml',
        'security/ir_model_access.xml',
        'security/ir_rule.xml',
        # views
        'views/formio_builder_views.xml',
        'views/formio_form_views.xml',
        'views/formio_res_model_views.xml',
        'views/formio_translation_source_views.xml',
        'views/formio_translation_views.xml',
        'views/formio_version_views.xml',
        'views/formio_menu.xml',
        # formio templates
        'views/formio_builder_templates.xml',
        'views/formio_form_templates.xml',
        'views/formio_portal_templates.xml',
    ],
    'installable': True,
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Form.io
=======

Build, deploy and store web forms in with the "Form.io" Form Builder.

http://form.io

The "Form.io" GUI/renderer and data are hosted on-premise (your hosting). So you're under control.

After installation of the module you can start right away.
No extra setup and requirements are needed.

Form Builder
------------

* Form Building starts in Odoo, by create a record and open the Form Builder right away.
* All Form data (schema) is stored on-premise, in your Odoo database

Form
----

* Users can create, edit and fill-in Forms.
* Forms are stored in the Odoo database.

"""
}
