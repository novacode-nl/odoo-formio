# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io',
    'summary': 'Form.io integration',
    'version': '0.1',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['website', 'base'],
    'data': [
        'views/formio_builder_views.xml',
        'views/formio_menu.xml',
        'views/formio_templates.xml'
    ],
    'application': True,
    'description': """
Form.io integration
====================

After installation you can start right away!
No extra installation or setup is required.

Form Builder
------------

* Deployed and ready to use. Just create and edit a Form (Builder) from within Odoo.
* Form schema/data is tored in your Odoo database upon each change.

"""
}
