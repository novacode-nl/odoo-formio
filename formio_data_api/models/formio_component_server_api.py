# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class FormioComponentServerApi(models.Model):
    _name = 'formio.component.server.api'
    _description = 'Formio Component Server API'

    DEFAULT_PYTHON_CODE = """# Available variables:
#  - value: Dictionary, read by the Forms Data API to set the Component(s) value.
#  - env: Odoo Environment on which the action is triggered
#  - component: Form component (formiodata.Component) object
#  - record: formio.form record on which the action is triggered; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
# Assign to values (dict), eg values['foo'] = 'bar', values.update({some_dict})"""

    formio_builder_id = fields.Many2one(
        'formio.builder', string='Form Builder',
        required=True, readonly=True, ondelete='cascade')
    name = fields.Char(string='API Name', required=True)
    # Python code
    code = fields.Text(
        string='Python Code', groups='base.group_system',
        default=DEFAULT_PYTHON_CODE,
        help="Write Python code that the Component Value will get set. Some variables are "
        "available for use; help about python expression is given in the help tab.")
    active = fields.Boolean(string='Active')
