# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields


def monkey_patch(cls):
    """ Return a method decorator to monkey-patch the given class. """
    def decorate(func):
        name = func.__name__
        func.super = getattr(cls, name, None)
        setattr(cls, name, func)
        return func
    return decorate

@monkey_patch(fields.Html)
def convert_to_cache(self, value, record, validate=True):
    if not record._context.get('website_id'):
        return convert_to_cache.super(self, value, record, validate=True)
    else:
        try:
            unsanitize_config_model = record.env['website.editor.unsanitize.html.field'].sudo()
        except:
            return convert_to_cache.super(self, value, record, validate=True)

        domain = [('model_field', '=', self)]
        if record._context.get('website_id') and unsanitize_config_model.search_count(domain) > 0:
            validate = False
        else:
            validate = True
        return convert_to_cache.super(self, value, record, validate=validate)
