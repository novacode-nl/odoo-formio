# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Form.io Reports Generator',
    'summary': 'Generate (PDF) reports for every Form',
    'version': '0.4',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': ['formio', 'formio_data_api'],
    'data': [
        'report/formio_form_report_views.xml',
        'report/report_formio_form.xml',
        'report/report_formio_form_components.xml',
        'security/ir_model_access.xml',
        'views/formio_builder_views.xml',
        'views/formio_builder_report_views.xml'
    ],
    'application': False,
    'images': [
        'static/description/banner.png',
    ],
}
