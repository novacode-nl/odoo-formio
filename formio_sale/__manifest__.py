# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io - Sales',
    'summary': 'Form.io webforms on Sale Orders',
    'version': '0.1',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['sale', 'formio'],
    'data': [
        'views/sale_views.xml',
        # 'views/formio_form_views.xml',
        # 'views/formio_menu.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Form.io Sales
=============
"""
}
