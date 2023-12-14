# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging

from io import BytesIO
from os.path import dirname

try:
    from werkzeug.utils import send_file
except ImportError:
    from odoo.tools._vendor.send_file import send_file

from odoo import http, fields
from odoo.http import request

from ..models.formio_form import (
    STATE_DRAFT as FORM_STATE_DRAFT,
    STATE_COMPLETE as FORM_STATE_COMPLETE,
)
from .utils import generate_uuid4, log_form_submisssion, validate_csrf

_logger = logging.getLogger(__name__)


class FormioController(http.Controller):

    ##############
    # Form Builder
    ##############

    @http.route('/formio/builder/<int:builder_id>', type='http', auth='user', website=True)
    def builder_root(self, builder_id, **kwargs):
        if not request.env.user.has_group('formio.group_formio_admin'):
            # TODO Render template with message?
            return request.redirect("/")

        # TODO REMOVE (still needed or obsolete legacy?)
        # Needed to update language
        context = request.env.context.copy()
        context.update({'lang': request.env.user.lang})
        request.env.context = context

        builder = request.env['formio.builder'].browse(builder_id)
        languages = builder.languages
        lang_en = request.env.ref('base.lang_en')

        if lang_en.active and builder.language_en_enable and 'en_US' not in languages.mapped('code'):
            languages |= request.env.ref('base.lang_en')

        values = {
            'builder': builder,
            # 'languages' already injected in rendering somehow
            'builder_languages': languages,
            'formio_css_assets': builder.formio_css_assets,
            'formio_js_assets': builder.formio_js_assets,
            'extra_assets': builder.extra_asset_ids,
            # uuid is used to disable assets (js, css) caching by hrefs
            'uuid': generate_uuid4()
        }
        return request.render('formio.formio_builder_embed', values)

    @http.route('/formio/builder/<int:builder_id>/config', type='http', auth='user', methods=['POST'], csrf=False, website=True)
    def builder_config(self, builder_id):
        if not request.env.user.has_group('formio.group_formio_admin'):
            return
        builder = request.env['formio.builder'].browse(builder_id)
        res = {'schema': {}, 'options': {}}

        if builder:
            if builder.schema:
                res['schema'] = json.loads(builder.schema)
            res['options'] = builder._get_js_options()
            res['params'] = builder._get_js_params()
            res['locales'] = builder._get_form_js_locales()
            res['csrf_token'] = request.csrf_token()
        return request.make_json_response(res)

    @http.route('/formio/builder/<model("formio.builder"):builder>/save', type='http', auth="user", methods=['POST'], csrf=False, website=True)
    def builder_save(self, builder):
        self.validate_csrf()
        if not request.env.user.has_group('formio.group_formio_admin'):
            return

        post = request.get_json_data()
        if 'builder_id' not in post or int(post['builder_id']) != builder.id:
            return

        schema = json.dumps(post['schema'])
        builder.write({'schema': schema})

    #######################
    # Form - backend - uuid
    #######################

    @http.route('/formio/form/<string:uuid>', type='http', auth='user', website=True)
    def form_root(self, uuid):
        form = self._get_form(uuid, 'read')
        if not form:
            msg = 'Form UUID %s' % uuid
            return request.not_found(msg)

        # TODO REMOVE (still needed or obsolete legacy?)
        # Needed to update language
        context = request.env.context.copy()
        context.update({'lang': request.env.user.lang})
        request.env.context = context

        languages = form.builder_id.languages
        lang_en = request.env.ref('base.lang_en')

        if lang_en.active and form.builder_id.language_en_enable and 'en_US' not in languages.mapped('code'):
            languages |= request.env.ref('base.lang_en')

        values = {
            'form': form,
            # 'languages' already injected in rendering somehow
            'form_languages': languages.sorted('name'),
            'formio_css_assets': form.builder_id.formio_css_assets,
            'formio_js_assets': form.builder_id.formio_js_assets,
            'extra_assets': form.builder_id.extra_asset_ids,
            # uuid is used to disable assets (js, css) caching by hrefs
            'uuid': generate_uuid4()
        }
        return request.render('formio.formio_form_embed', values)

    @http.route('/formio/form/<string:form_uuid>/config', type='http', auth='user', csrf=False, website=True)
    def form_config(self, form_uuid):
        form = self._get_form(form_uuid, 'read')
        # TODO remove config (key)
        res = {'schema': {}, 'options': {}, 'config': {}, 'params': {}}

        if form and form.builder_id.schema:
            res['schema'] = json.loads(form.builder_id.schema)
            res['options'] = self._get_form_js_options(form)
            res['params'] = self._get_form_js_params(form)
            res['locales'] = self._get_form_js_locales(form)
            res['csrf_token'] = request.csrf_token()
        return request.make_json_response(res)

    @http.route('/formio/form/<string:uuid>/submission', type='http', auth='user', csrf=False, website=True)
    def form_submission(self, uuid):
        form = self._get_form(uuid, 'read')

        # Submission data
        if form and form.submission_data:
            submission_data = json.loads(form.submission_data)
        else:
            submission_data = {}

        # ETL Odoo data
        if form:
            etl_odoo_data = form.sudo()._etl_odoo_data()
            submission_data.update(etl_odoo_data)

        return request.make_json_response(submission_data)

    @http.route('/formio/form/<string:uuid>/submit', type='http', auth="user", methods=['POST'], csrf=False, website=True)
    def form_submit(self, uuid):
        """ POST with ID instead of uuid, to get the model object right away """
        self.validate_csrf()
        form = self._get_form(uuid, 'write')
        if not form or form.state == FORM_STATE_COMPLETE:
            # TODO raise or set exception (in JSON resonse) ?
            return
        post = request.get_json_data()
        vals = {
            'submission_data': json.dumps(post['data']),
            'submission_user_id': request.env.user.id,
            'submission_date': fields.Datetime.now(),
        }

        if post.get('saveDraft') or (
            post['data'].get('saveDraft') and not post['data'].get('submit')
        ):
            vals['state'] = FORM_STATE_DRAFT
        else:
            vals['state'] = FORM_STATE_COMPLETE

        form.write(vals)

        if vals.get('state') == FORM_STATE_COMPLETE:
            form.after_submit()
        elif vals.get('state') == FORM_STATE_DRAFT:
            form.after_save_draft()

        # debug mode is checked/handled
        log_form_submisssion(form)

        res = {
            'form_uuid': uuid,
            'submission_data': form.submission_data
        }
        return request.make_json_response(res)

    #######
    # Fonts
    #######

    @http.route(['/web/content/<int:id>/fonts/<string:name>'], type='http', auth="public")
    def send_fonts_file(self, id, name, **kwargs):
        """
        WARNING
        -------
        This route (/fonts/) is a rather iffy assumption which could
        cause troubles.  Of course this could be requested by other
        parts, but not yet in standard Odoo routes.

        ----------------------------------------------------------
        TODO DeprecationWarning, odoo.http.send_file is deprecated
        ----------------------------------------------------------
        But:
        http.Stream.from_path only obtains the addons_path, not
        filestore!

        stream = http.Stream.from_path(fontfile_path)
        return stream.get_response()

        Workaround: (to improve/replace in future?)
        still using Odoo <= v15 approach by using Werkzeug
        implementation
        ----------------------------------------------------------

        :param int id: The ID of the file (attachment) which requests the fonts file.
            File(s) requesting this font file, are CSS files (formio.js library).
        :param str name: The name of the fontfile in request.
        """

        ir_attach = request.env['ir.attachment'].sudo()
        attach = ir_attach.browse(id)
        if not attach.formio_asset_formio_version_id:
            msg = 'Request expects a Forms (formio.js) fonts file (id: %s, name: %s' % (id, name)
            _logger.warning(msg)
            return request.not_found(msg)
        attachment_location = request.env['ir.attachment']._storage()
        if attachment_location == 'file':
            attach_dir = dirname(attach.store_fname)
            fonts_dir = '{attach_dir}/fonts/'.format(attach_dir=attach_dir)
            fontfile_path = request.env['ir.attachment']._full_path(fonts_dir)
            fontfile_path += '/%s' % name
            return send_file(fontfile_path, request.httprequest.environ)
        else:
            # Get the font-file via formio.version.asset;
            # don't search ir.attachment directly, as there are no indexes on formio_asset_formio_version_id
            assets = request.env["formio.version.asset"].search(
                [
                    ("version_id", "=", attach.formio_asset_formio_version_id.id),
                ])
            font_asset = assets.filtered(lambda a: a.attachment_id.name == name)
            if not font_asset:
                msg = f"Font {name} not found"
                _logger.warning(msg)
                return request.not_found(msg)
            return send_file(BytesIO(font_asset.attachment_id.raw), request.httprequest.environ, download_name=name)

    #########
    # Helpers
    #########

    def _get_form_js_options(self, form):
        options = form._get_js_options()

        # language
        Lang = request.env['res.lang']
        if request.env.user.lang in form.languages.mapped('code'):
            language = Lang._formio_ietf_code(request.env.user.lang)
        else:
            language = Lang._formio_ietf_code(request.env.context['lang'])
        options['language'] = language
        return options

    def _get_form_js_locales(self, form):
        return form.builder_id._get_form_js_locales()

    def _get_form_js_params(self, form):
        return form._get_js_params()

    def _get_form(self, uuid, mode):
        return request.env['formio.form'].get_form(uuid, mode)

    def validate_csrf(self):
        validate_csrf(request)
