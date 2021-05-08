# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

from odoo.addons.mail.models.mail_render_mixin import MailRenderMixin


def _formio(model_obj):
    """
    Return Form (or Builder) object by formio_data_api.
    
    This is needed, because the Jinja Sandbox object, doesn't allow
    the ${object._formio} which it treats as unsafe and throws an
    exception.
    
    USAGE EXAMPLE (e.g. in mail.template)
    -------------------------------------
    ${formio(object).data.firstName.value}
    """
    formio = model_obj._formio
    return formio

def monkey_patch(cls):
    """ Return a method decorator to monkey-patch the given class. """
    def decorate(func):
        name = func.__name__
        func.super = getattr(cls, name, None)
        setattr(cls, name, func)
        return func
    return decorate


@monkey_patch(MailRenderMixin)
def _render_jinja_eval_context(self):
    """ Prepare jinja evaluation context, containing for all rendering
    various formatting tools """
    res = _render_jinja_eval_context.super(self)
    res['formio'] = lambda model_obj: _formio(model_obj)
    return res
