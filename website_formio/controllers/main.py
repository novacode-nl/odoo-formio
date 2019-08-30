# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo.http import route, request, Controller
from odoo.addons.formio.controllers.main import FormioController


class FormioWebsiteController(FormioController):

    def _prepare_form_options(self, form):
        options = super(FormioWebsiteController, self)._prepare_form_options(form)
        if form.builder_id.submit_done_page:
            options['submitDone'] = {'url': form.builder_id.submit_done_page.url}
        return options
