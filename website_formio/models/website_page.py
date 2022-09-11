# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug


class WebsitePage(models.Model):
    _name = 'formio.website.page'
    _description = 'Forms Website Page'
    _inherit = ['mail.thread', 'website.published.multi.mixin']

    # see also (odoo CE):
    # - website_sale: product.template
    name = fields.Char(required=True, tracking=True, copy=False)
    formio_builder_id = fields.Many2one(
        comodel_name="formio.builder",
        string="Form Builder",
        domain=[("public", "=", True)],
        tracking=True,
        copy=False,
    )
    website_content_1 = fields.Html(sanitize=False)
    website_content_2 = fields.Html(sanitize=False)

    @api.depends('name')
    def _compute_website_url(self):
        super(WebsitePage, self)._compute_website_url()
        for page in self:
            if page.id:
                page.website_url = '/website/formio/%s' % slug(page)
