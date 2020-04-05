# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Report PDF',
    'summary': 'Form.io module to create pdf reports from webforms',
    'version': '0.1',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Reporting',
    'depends': ['formio'],
    'data': [
        'views/formio_form_templates.xml',
    ],
    'application': True,
    'images': [
        'static/description/banner.png',
    ],
    'description': """
Form.io - Export to PDF
==================

Exports PDFs from Form.io webforms.
"""
}
