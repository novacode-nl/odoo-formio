# Copyright 2022 Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import http
from odoo.http import request

from odoo.addons.formio.controllers.public import FormioPublicController

import logging
_logger = logging.getLogger(__name__)


class WebsiteController(FormioPublicController):

    @http.route(['/website/formio/<model("formio.website.page"):page>'], type='http', auth='public', website=True, sitemap=False)
    def forms_page(self, page, **kwargs):
        can_admin = request.env.user.has_group("website.group_website_designer")
        if not can_admin and not page.is_published:
            return request.render('http_routing.404')

        values = {
            'page': page,
            'form': False,
            'main_object': page,
        }

        if 'form' in kwargs:
            form_uuid = kwargs.get('form')
            form = self._get_public_form(form_uuid, self._check_public_form())
            if not form or page.id not in form.builder_id.formio_website_page_ids.ids:
                return request.render('http_routing.404')
            else:
                values['form'] = {
                    'form': form,
                    'form_url': '/formio/public/form/%s' % form.uuid
                }
        else:
            builder = page.sudo().formio_builder_id
            if builder.public:
                values['form'] = {
                    'form_url': '/formio/public/form/create/%s' % builder.uuid
                }
        return request.render('website_formio.formio_website_page', values)
