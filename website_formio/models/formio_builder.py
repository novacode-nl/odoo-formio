# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class Builder(models.Model):
    _name = 'formio.builder'
    _inherit = ['formio.builder', 'website.published.multi.mixin']

    portal_submit_done_page_id = fields.Many2one(
        'website.page', domain=[('is_published', '=', True), ('url', '!=', '/')],
        string='Portal Submit-done Page', tracking=True)
    public_submit_done_page_id = fields.Many2one(
        'website.page', domain=[('is_published', '=', True), ('url', '!=', '/')],
        string='Public Submit-done Page', tracking=True)
    formio_website_page_ids = fields.One2many(
        "formio.website.page", string="Website Pages", compute='_compute_website_pages'
    )

    @api.model
    def create(self, vals):
        portal_submit_done_page_id = vals.get('portal_submit_done_page_id')
        if portal_submit_done_page_id:
            portal_submit_done_page = self.env['website.page'].browse(portal_submit_done_page_id)
            vals['portal_submit_done_url'] = portal_submit_done_page.url

        public_submit_done_page_id = vals.get('public_submit_done_page_id')
        if public_submit_done_page_id:
            public_submit_done_page = self.env['website.page'].browse(public_submit_done_page_id)
            vals['public_submit_done_url'] = public_submit_done_page.url

        return super(Builder, self).create(vals)

    def write(self, vals):
        portal_submit_done_page_id = vals.get('portal_submit_done_page_id')
        if portal_submit_done_page_id:
            portal_submit_done_page = self.env['website.page'].browse(portal_submit_done_page_id)
            vals['portal_submit_done_url'] = portal_submit_done_page.url

        public_submit_done_page_id = vals.get('public_submit_done_page_id')
        if public_submit_done_page_id:
            public_submit_done_page = self.env['website.page'].browse(public_submit_done_page_id)
            vals['public_submit_done_url'] = public_submit_done_page.url

        return super(Builder, self).write(vals)

    def _compute_website_pages(self):
        pages = self.env['formio.website.page'].search([('formio_builder_id', 'in', self.ids)])
        for r in self:
            builder_pages = pages.filtered(lambda p: p.formio_builder_id.id == r.id)
            r.formio_website_page_ids = [(6, 0, builder_pages.ids)]

    @api.onchange('portal_submit_done_page_id')
    def _onchange_portal_submit_done_page(self):
        if not self.portal_submit_done_page_id:
            self.portal_submit_done_url = False
        else:
            self.portal_submit_done_url = self.portal_submit_done_page_id.url

    @api.onchange('public_submit_done_page_id')
    def _onchange_public_submit_done_page(self):
        if not self.public_submit_done_page_id:
            self.public_submit_done_url = False
        else:
            self.public_submit_done_url = self.public_submit_done_page_id.url
