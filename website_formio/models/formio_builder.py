# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class Builder(models.Model):
    _inherit = 'formio.builder'

    submit_done_page_id = fields.Many2one('website.page', domain=[('is_published', '=', True), ('url', '!=', '/')])
    portal_submit_done_page_id = fields.Many2one('website.page', domain=[('is_published', '=', True), ('url', '!=', '/')])

    @api.model
    def create(self, vals):
        submit_done_page_id = vals.get('submit_done_page_id')
        portal_submit_done_page_id = vals.get('portal_xsubmit_done_page_id')
        if submit_done_page_id:
            submit_done_page = self.env['website.page'].browse(submit_done_page_id)
            vals['submit_done_url'] = submit_done_page.url
        if portal_submit_done_page_id:
            portal_submit_done_page = self.env['website.page'].browse(portal_submit_done_page_id)
            vals['portal_submit_done_url'] = portal_submit_done_page.url
        return super(Builder, self).create(vals)

    @api.multi
    def write(self, vals):
        submit_done_page_id = vals.get('submit_done_page_id')
        portal_submit_done_page_id = vals.get('portal_submit_done_page_id')
        if submit_done_page_id:
            submit_done_page = self.env['website.page'].browse(submit_done_page_id)
            vals['submit_done_url'] = submit_done_page.url
        if portal_submit_done_page_id:
            portal_submit_done_page = self.env['website.page'].browse(portal_submit_done_page_id)
            vals['portal_submit_done_url'] = portal_submit_done_page.url
        return super(Builder, self).write(vals)

    @api.onchange('submit_done_page_id')
    def _onchange_submit_done_page(self):
        if not self.submit_done_page_id:
            self.submit_done_url = False
        else:
            self.submit_done_url = self.submit_done_page_id.url

    @api.onchange('portal_submit_done_page_id')
    def _onchange_portal_submit_done_page(self):
        if not self.portal_submit_done_page_id:
            self.portal_submit_done_url = False
        else:
            self.portal_submit_done_url = self.portal_submit_done_page_id.url
