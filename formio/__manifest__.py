# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io',
    'summary': 'Build, publish and store webforms in Odoo with the "Form.io" GUI/renderer',
    'version': '0.1',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['web', 'mail'],
    'data': [
        'security/formio_security.xml',
        'security/ir_model_access.xml',
        'views/formio_builder_views.xml',
        'views/formio_builder_templates.xml',
        'views/formio_form_views.xml',
        'views/formio_form_templates.xml',
        'views/formio_menu.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Form.io integration
====================

Design and serve "Form.io" webforms, while manage and store its data in Odoo.

=> http://form.io

After installation you can start right away!
No extra installation or setup is required.

Form Builder
------------

* Deployed and ready to use. Just create and edit a Form Builder, which starts in Odoo.
* Form schema/data is stored in your Odoo database upon each change.

Form
----

* Users can create, edit and fill-in Forms.
* Forms are stored in the Odoo database.

"""
}
