# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    "name": "Form.io Reports Generator",
    'summary': 'Generate reports from Form.io webforms (by QWeb)',
    "version": "0.1",
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    "license": "LGPL-3",
    'category': 'Extra Tools',
    "depends": ["formio", "formio_data_api"],
    "data": [
        'report/formio_form_report_views.xml',
        'report/report_formio_form.xml',
        'report/report_formio_form_components.xml',
    ],
    "application": False,
    'images': [
        'static/description/banner.png',
    ],
}
