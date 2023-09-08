# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import base64
import logging
import os
import requests
import shutil
import tarfile

from odoo import api, fields, models

logger = logging.getLogger(__name__)

STATE_AVAILABLE = 'available'
STATE_INSTALLED = 'installed'

STATES = [(STATE_AVAILABLE, "Available"), (STATE_INSTALLED, "Installed")]


class VersionGitHubTag(models.Model):
    _name = 'formio.version.github.tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'formio.js Version GitHub Tag'
    #_order = 'create_date desc, id asc'
    order = 'write_date desc, id desc'

    # IMPORTANT NOTES
    # ===============
    # formio.js published release ain't available with the GitHub releases API
    # https://developer.github.com/v3/repos/releases/#list-releases
    #
    # GitHub tags API:
    # https://developer.github.com/v3/repos/#list-repository-tags
    # - Results per page (max 100)
    # - Sorted by tag name (descending)

    name = fields.Char(required=True)

    version_name = fields.Char(compute='_compute_fields')
    formio_version_id = fields.Many2one('formio.version', string='formio.js version')
    archive_url = fields.Char(compute='_compute_fields', string="Archive URL")
    changelog_url = fields.Char(compute='_compute_fields', string="Changelog URL")
    state = fields.Selection(
        selection=STATES, string="State",
        default=STATE_AVAILABLE, required=True, tracking=True,
        help="""\
        - Available: Not downloaded and installed yet.
        - Installed: Downloaded and installed.""")
    install_date = fields.Datetime(string='Installed on', compute='_compute_install_date', store=True)

    @api.depends('name')
    def _compute_fields(self):
        for r in self:
            if r.name:
                r.archive_url = 'https://github.com/formio/formio.js/archive/%s.tar.gz' % r.name
                r.changelog_url = 'https://github.com/formio/formio.js/blob/%s/Changelog.md' % r.name
                r.version_name = r.name[1:]
            else:
                r.archive_url = False
                r.changelog_url = False
                r.version_name = False

    @api.depends('state')
    def _compute_install_date(self):
        for r in self:
            if r.state == STATE_INSTALLED:
                r.install_date = fields.Datetime.now()
            else:
                r.install_date = False

    @api.model
    def check_and_register_available_versions(self):
        vals_list = self.env['formio.version.github.checker.wizard'].check_new_versions()
        if vals_list:
            self.create(vals_list)

    def action_download_install(self):
        # NOTICE: no windows (path) support
        #
        # See also comment in `ir.attachment` its
        # `_get_path` function:
        #     we use '/' in the db (even on windows)

        if self.formio_version_id:
            return

        # dirs, paths
        IrAttachment = self.env['ir.attachment']
        archive_dir = 'formiojs/archive'
        archive_path = IrAttachment._full_path(archive_dir)

        if not os.path.isdir(archive_path):
            os.makedirs(archive_path)

        src_dir = 'formiojs/src'
        src_path = IrAttachment._full_path(src_dir)

        if not os.path.isdir(src_path):
            os.makedirs(src_path)

        src_version_path = '%s/formio.js-%s' % (src_path, self.version_name)
        tar_path = '%s/%s.tar.gz' % (archive_path, self.version_name)

        logger.info('version path => %s' % src_version_path)
        logger.info('archive (.tar.gz) path => %s' % tar_path)

        # download
        response = requests.get(self.archive_url, stream=True)
        logger.info('download => %s' % self.archive_url)

        if response.status_code == 200:
            with open(tar_path, 'wb') as f:
                f.write(response.raw.read())
                tar = tarfile.open(tar_path)
                tar.extractall(src_path, members=self._tar_extract_members(tar))
                tar.close()

            version_model = self.env['formio.version'].sudo()
            asset_model = self.env['formio.version.asset'].sudo()
            attachment_model = self.env['ir.attachment']

            # First delete if any already. If repeating download/install.
            domain = [('name', '=', self.version_name)]
            version_model.search(domain).unlink()

            vals = {
                'name': self.version_name,
            }
            version = version_model.create(vals)
            version.action_add_base_translations()

            ################
            # default assets
            ###############
            assets_vals_list = []
            default_assets_css = self.env['formio.default.asset.css'].search([])
            for css in default_assets_css:
                default_asset_vals = {
                    'version_id': version.id,
                    'attachment_id': css.attachment_id.id,
                    'type': 'css'
                }
                assets_vals_list.append(default_asset_vals)

            ###################################################
            # https://github.com/formio/formio.js - LICENSE.txt
            ###################################################
            license_filename = 'LICENSE.txt'
            license_path = '%s/%s' % (src_version_path, license_filename)

            # attachment
            if os.path.exists(license_path):
                attachment_vals = self._prepare_version_asset_attachment_vals(version, license_filename, license_path)
                attachment = attachment_model.create(attachment_vals)
                asset_vals = {
                    'version_id': version.id,
                    'attachment_id': attachment.id,
                    'type': 'license'
                }
                assets_vals_list.append(asset_vals)

            ###########################################
            # assets: js, css, fonts, formio.js LICENSE
            ###########################################

            attachment_location = IrAttachment._storage()
            dist_version_path = '%s/dist' % src_version_path

            for root, dirs, files in os.walk(dist_version_path):
                for fname in files:
                    dist_file = '%s/%s' % (root, fname)
                    # target_file = '%s/%s' % (static_version_dir, fname)
                    # shutil.move(original_file, target_file)

                    logger.debug(f"add asset={fname}")
                    file_ext = os.path.splitext(fname)[1]
                    # drop leading dot '.'
                    file_ext = file_ext.split(".")[-1]

                    if fname == 'formio.full.min.js.LICENSE.txt':
                        ######################################################################
                        # https://github.com/formio/formio.js - formio.full.min.js.LICENSE.txt
                        ######################################################################

                        # TODO: with open(original_file):
                        license_file = open(dist_file, 'rb')
                        attachment_vals = {
                            'name': fname,
                            'type': 'binary',
                            'datas': base64.b64encode(license_file.read())
                        }
                        license_file.close()
                        attachment = attachment_model.create(attachment_vals)

                        asset_vals = {
                            'version_id': version.id,
                            'attachment_id': attachment.id,
                            'type': 'license'
                        }
                        assets_vals_list.append(asset_vals)
                        continue
                    else:
                        attachment_vals = self._prepare_version_asset_attachment_vals(version, fname, dist_file)
                        attachment = IrAttachment.create(attachment_vals)
                        asset_vals = {
                            "version_id": version.id,
                            "attachment_id": attachment.id,
                            "type": file_ext
                        }
                        assets_vals_list.append(asset_vals)
                    # fonts if 'file' storage
                    if attachment_location == 'file' and file_ext == 'css':
                        # copy other (font) files if attachments are stored statically in filestore
                        src_fonts_path = '%s/dist/fonts' % src_version_path
                        css_attach_dir = os.path.dirname(attachment.store_fname)
                        css_attach_path = IrAttachment._full_path(css_attach_dir)
                        target_fonts_path = '%s/fonts' % css_attach_path
                        # XXX this leads to troubles if formio.js
                        # versions ship different font files (version dependent).
                        # However, the CSS url to resolve the fonts is expected to be
                        # this precise one.
                        if os.path.exists(src_fonts_path) and not os.path.exists(target_fonts_path):
                            shutil.copytree(src_fonts_path, target_fonts_path)


            if assets_vals_list:
                res = asset_model.create(assets_vals_list)
                for rec in res:
                    attachment_vals = {
                        'res_model': 'formio.version.asset',
                        'res_id': rec.id
                    }
                    rec.attachment_id.write(attachment_vals)

            ####################
            # cleanup and update
            ####################
            # dir
            shutil.rmtree(src_version_path)
            # file (*.tar.gz)
            os.remove(tar_path)
            self.write({'state': STATE_INSTALLED, 'formio_version_id': version.id})

    def _prepare_version_asset_attachment_vals(self, version, file_name, file_path):
        with open(file_path, "rb") as f:
            attachment_vals = {
                "name": file_name,
                "type": "binary",
                "public": True,
                "formio_asset_formio_version_id": version.id,
                "datas": base64.b64encode(f.read())
            }
        return attachment_vals

    def action_reset_installed(self):
        if self.formio_version_id:
            vals = {'formio_version_id': False, 'state': STATE_AVAILABLE}
            self.write(vals)
            self.action_download_install()

    def _tar_extract_members(self, members):
        full_todo = ['formio.full.min.js', 'formio.full.min.css', 'LICENSE.txt', 'formio.full.min.js.LICENSE.txt']
        full_done = []

        # In case minimized files not found
        src = {'formio.full.min.js': 'formio.js', 'formio.full.min.css': 'formio.full.css'}
        src_todo = []

        for tarinfo in members:
            basename = os.path.basename(tarinfo.name)
            dirname = os.path.dirname(tarinfo.name)

            dir_1 = os.path.basename(dirname)
            dir_2 = os.path.basename(os.path.dirname(dirname))

            if basename in full_todo:
                logger.info('tar extract member => %s' % basename)
                full_done.append(basename)
                yield tarinfo
            # elif dir_1 == 'dist' and dir_2 == 'dist':
            #     logger.info('tar extract => dist/fonts')
            #     yield tarinfo
            elif dir_1 == 'fonts' and dir_2 == 'dist':
                logger.info('tar extract => dist/fonts %s' % basename)
                yield tarinfo

        # In case minimized files not found
        src_todo = [src[todo] for todo in full_todo if todo not in full_done and src.get(todo)]
        for tarinfo in members:
            filename = os.path.basename(tarinfo.name)
            if filename in src_todo:
                logger.info('tar extract member => %s' % filename)
                yield tarinfo
