# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import ast
import json
import re
import uuid

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.http import request

from ..utils import get_field_selection_label

STATE_DRAFT = 'DRAFT'
STATE_CURRENT = 'CURRENT'
STATE_OBSOLETE = 'OBSOLETE'

STATES = [
    (STATE_DRAFT, "Draft"),
    (STATE_CURRENT, "Current"),
    (STATE_OBSOLETE, "Obsolete")]


class Builder(models.Model):
    _name = 'formio.builder'
    _description = 'Form Builder'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _order = 'title'
    _rec_name = 'display_name_full'

    _interval_selection = {'minutes': 'Minutes', 'hours': 'Hours', 'days': 'Days'}
    _public_access_rule_types = {'time_interval': 'Time Interval'}

    name = fields.Char(
        "Name", required=True, tracking=True,
        help="""Identifies this specific form. This name can be used in APIs. \
        Use only ASCII letters, digits, "-" or "_".""")
    uuid = fields.Char(
        default=lambda self: self._default_uuid(), required=True, readonly=True, copy=False,
        string='UUID')
    title = fields.Char(
        "Title", required=True,
        help="The form title in the current language", tracking=True)
    description = fields.Text("Description")
    formio_version_id = fields.Many2one(
        'formio.version', string='formio.js version', required=True,
        default=lambda self: self._default_formio_version_id(), tracking=True,
        help="""Loads the specific formio.js Javascript libraries version (sourcecode: https://github.com/formio/formio.js)""")
    formio_version_name = fields.Char(related='formio_version_id.name', string='formio.js version name', tracking=False)  # silly, but avoids duplicate tracking message
    formio_version_is_dummy = fields.Boolean(related='formio_version_id.is_dummy')
    formio_css_assets = fields.One2many(related='formio_version_id.css_assets', string='formio.js CSS')
    formio_js_assets = fields.One2many(related='formio_version_id.js_assets', string='formio.js Javascript')
    extra_asset_ids = fields.Many2many(
        comodel_name='formio.extra.asset',
        string='Extra Assets',
        domain=[('attachment_id.res_model', '=', 'formio.extra.asset')]
    )
    formio_js_options_id = fields.Many2one('formio.builder.js.options', string='formio.js Javascript Options template', store=False)
    formio_js_options = fields.Text(
        default=lambda self: self._default_formio_js_options(),
        string='formio.js Javascript Options')
    res_model_id = fields.Many2one(
        "ir.model", compute='_compute_res_model_id', store=True,
        string="Model", help="Model as resource this form represents or acts on")
    res_model = fields.Char(compute='_compute_res_model_id', store=True)
    formio_res_model_id = fields.Many2one(
        "formio.res.model",
        string="Resource Model",
        ondelete='restrict', tracking=True,
        help="Model as resource this form represents or acts on")
    schema = fields.Text("JSON Schema")
    edit_url = fields.Char(compute='_compute_edit_url', readonly=True)
    act_window_url = fields.Char(compute='_compute_act_window_url', readonly=True)
    state = fields.Selection(
        selection=STATES, string="State",
        default=STATE_DRAFT, required=True, tracking=True,
        help="""\
        - Draft: In draft / design.
        - Current: Live and in use (published).
        - Obsolete: Was current but obsolete (unpublished)""")
    display_state = fields.Char("Display State", compute='_compute_display_fields', store=False)
    display_name_full = fields.Char("Display Name Full", compute='_compute_display_fields', search='_search_display_name_full', store=False)
    auto_save = fields.Boolean(
        string="Auto Save",
        default=True,
        tracking=True,
        help="Auto-save or manually save the Form Builder changes",
    )
    is_locked = fields.Boolean(
        string="Locked", copy=False, tracking=True,
        help="""\
        - Locked: No further modifications are possible in the Form Builder and configuration.
        - Unlocked: Modications are possible, but could cause existing forms to be invalid.""")
    parent_id = fields.Many2one('formio.builder', string='Parent Builder', readonly=True)
    parent_version = fields.Integer(related='parent_id.version', string='Parent Version', readonly=True)
    version = fields.Integer("Version", required=True, readonly=True, default=1)
    version_comment = fields.Text("Version Comment")
    user_id = fields.Many2one('res.users', string='Assigned user', tracking=True)  # TODO old field, remove?
    forms = fields.One2many('formio.form', 'builder_id', string='Forms')
    forms_count = fields.Integer(string='Forms Count', compute='_compute_forms_count')
    backend_use_draft = fields.Boolean(
        string='Use Draft in Backend',
        default=False,
        help='Allows to use this Form Builder in state Draft, when adding/choosing a new Form in the backend.'
    )
    backend_use_obsolete = fields.Boolean(
        string='Use Obsolete in Backend',
        default=False,
        help='Allows to use this Form Builder in state Obsolete, when adding/choosing a new Form in the backend.'
    )
    portal = fields.Boolean("Portal", tracking=True, help="Form is accessible by assigned portal user")
    portal_url = fields.Char(string='Portal URL', compute='_compute_portal_urls')
    portal_save_draft_done_url = fields.Char(
        string='Portal Save-Draft Done URL', tracking=True,
        help="""\
        IMPORTANT:
        - Absolute URL should contain a protocol (https://, http://)
        - Relative URL is also supported e.g. /web/login
        """
    )
    portal_submit_done_url = fields.Char(
        string='Portal Submit Done URL', tracking=True,
        help="""\
        IMPORTANT:
        - Absolute URL should contain a protocol (https://, http://)
        - Relative URL is also supported e.g. /web/login
        """
    )
    portal_scroll_into_view_selector = fields.Char(
        string='Portal Scroll Into View Selector',
        copy=False,
        tracking=True,
        help="Especially for long wizard pages upon prev/next page. This scrolls an element (CSS selector) into the visible area of the browser window."
    )
    public = fields.Boolean("Public", tracking=True, help="Form is public accessible (e.g. used in Shop checkout, Events registration")
    public_url = fields.Char(string='Public URL', compute='_compute_public_url')
    public_save_draft_done_url = fields.Char(
        string='Public Save-Draft Done URL', tracking=True,
        help="""\
        IMPORTANT:
        - Absolute URL should contain a protocol (https://, http://)
        - Relative URL is also supported e.g. /web/login
        """
    )
    public_submit_done_url = fields.Char(
        string='Public Submit Done URL', tracking=True,
        help="""\
        IMPORTANT:
        - Absolute URL should contain a protocol (https://, http://)
        - Relative URL is also supported e.g. /web/login
        """
    )
    public_access_rule_type = fields.Selection(
        list(_public_access_rule_types.items()),
        string='Public Access Rule Type',
        default='time_interval',
        tracking=True)
    public_access_interval_number = fields.Integer(default=30, tracking=True, help="Public access to submitted Form shall be rejected after expiration of the configured time interval.")
    public_access_interval_type = fields.Selection(list(_interval_selection.items()), default='minutes', tracking=True)
    public_scroll_into_view_selector = fields.Char(
        string='Public Scroll Into View Selector',
        copy=False,
        tracking=True,
        help="Especially for long wizard pages upon prev/next page. This scrolls an element (CSS selector) into the visible area of the browser window."
    )
    view_as_html = fields.Boolean("View as HTML", tracking=True, help="View submission as a HTML view instead of disabled webform.")
    show_form_title = fields.Boolean("Show Form Title", tracking=True, help="Show Form Title in the Form header.", default=True)
    show_form_id = fields.Boolean("Show Form ID", tracking=True, help="Show Form ID in the Form header.", default=True)
    show_form_uuid = fields.Boolean("Show Form UUID", tracking=True, help="Show Form UUID in the Form.", default=True)
    show_form_state = fields.Boolean("Show Form State", tracking=True, help="Show the state in the Form header.", default=True)
    show_form_user_metadata = fields.Boolean(
        "Show User Metadata", tracking=True, help="Show submission and assigned user metadata in the Form header.", default=True)
    iframe_resizer_body_margin = fields.Char(
        "iFrame Resizer bodyMargin", tracking=True,
        help="""\
        Override the default body margin style in the iFrame.
        A string can be any valid value for the CSS margin property.
        A number is converted into px.
        Example: 0px 0px 260px 0px
        """
    )
    wizard = fields.Boolean("Wizard", tracking=True)
    wizard_on_next_page_save_draft = fields.Boolean("Wizard on Next Page Save Draft", tracking=True)
    wizard_on_change_page_save_draft = fields.Boolean("Wizard on Change Page Save Draft", tracking=True)
    submission_url_add_query_params_from = fields.Selection(
        string="Add Query Params to Submission URL from",
        selection=[
            ("window", "Window iframe (src)"),
            ("window.parent", "Window parent (URL)"),
        ],
        tracking=True,
        help="Enables adding the URL query params from the window's iframe (src) or window.parent to the form submission URL endpoint.",
    )
    debug = fields.Boolean(
        string="Debug",
        default=False,
        copy=False,
        tracking=True,
        help="When enabled along the standard Developer Mode (debug mode), this provides server log output etc."
    )
    debug_mode = fields.Boolean(
        string="Debug Mode",
        compute='_compute_debug_mode'
    )
    translations = fields.One2many('formio.builder.translation', 'builder_id', string='Translations', copy=True)
    languages = fields.One2many('res.lang', compute='_compute_languages', string='Languages')
    allow_force_update_state_group_ids = fields.Many2many(
        'res.groups', string='Allow groups to force update State',
        help="User groups allowed to manually force an update of the Form state."
             "If no groups are specified it's allowed for every user.")
    language_en_enable = fields.Boolean(default=True, string='English Enabled')
    component_partner_name = fields.Char(string='Component Partner Name', tracking=True)
    component_partner_email = fields.Char(string='Component Partner Email', tracking=True)
    component_partner_add_follower = fields.Boolean(
        string='Component Partner Add to Followers', tracking=True, help='Add determined partner to followers of the Form.')
    component_partner_activity_user_id = fields.Many2one('res.users', tracking=True)
    form_allow_copy = fields.Boolean(string='Allow Copies', help='Allow copying form submissions.', tracking=True, default=True)
    form_copy_to_current = fields.Boolean(string='Copy To Current', help='When copying a form, always link it to the current version of the builder instead of the original builder.', tracking=True, default=True)
    server_action_ids = fields.Many2many(
        comodel_name='ir.actions.server',
        string='Server Actions',
        domain="[('model_name', '=', 'formio.form')]"
    )
    hook_api_validation = fields.Boolean(
        string='Hook Validation API', default=False, copy=True)
    overlay_api_change = fields.Boolean(
        string='Overlay Change API', default=False, copy=True)
    show_api_alert = fields.Boolean(compute='_compute_show_api_alert')
    api_alert = fields.Text(compute='_compute_api_alert')

    def _states_selection(self):
        return STATES

    @api.model
    def _default_uuid(self):
        return str(uuid.uuid4())

    @api.model
    def _default_formio_version_id(self):
        Param = self.env['ir.config_parameter'].sudo()
        default_version = Param.get_param('formio.default_version')
        if default_version:
            domain = [('name', '=', default_version)]
            version = self.env['formio.version'].search(domain, limit=1)
            if version:
                return version.id
            else:
                return False
        else:
            return False

    @api.model
    def _default_formio_js_options(self):
        Param = self.env['ir.config_parameter'].sudo()
        default_builder_js_options_id = Param.get_param('formio.default_builder_js_options_id')
        builder_js_options = self.env['formio.builder.js.options'].browse(int(default_builder_js_options_id))
        return builder_js_options.value

    @api.constrains('name')
    def constaint_check_name(self):
        for rec in self:
            if re.search(r"[^a-zA-Z0-9_-]", rec.name) is not None:
                raise ValidationError(_('Name is invalid. Use ASCII letters, digits, "-" or "_".'))

    @api.constrains("name", "state")
    def constraint_one_current(self):
        """ Per name there can be only 1 record with state current at
        a time. """

        res = self.search([
            ("name", "=", self.name),
            ("state", "=", STATE_CURRENT)
            ])
        if len(res) > 1:
            msg = _('Only one Form Builder with name "{name}" can be in state Current.').format(
                name=self.name)
            raise ValidationError(msg)

    @api.constrains("name", "version")
    def constraint_one_version(self):
        """ Per name there can be only 1 record with same version at a
        time. """

        domain = [('name', '=', self.name), ('version', '=', self.version)]
        res = self.search_count(domain)
        if res > 1:
            raise ValidationError("%s already has a record with version: %d. Use button/action: Create New Version."
                                  % (self.name, self.version))

    @api.constrains('public', 'public_access_rule_type')
    def constaint_public_access_rule_type(self):
        for rec in self:
            if rec.public and not rec.public_access_rule_type:
                raise ValidationError(_("The field 'Public Access Rule' Type is required for Public Forms!"))

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        name_suffix = fields.Datetime.to_string(fields.Datetime.now())
        name_suffix = name_suffix.replace(' ', '_')
        name_suffix = name_suffix.replace(':', '-')

        default = default or {}
        default['name'] = '%s_%s' % (self.name, name_suffix)
        return super(Builder, self).copy(default=default)

    def _decode_schema(self, schema):
        """ Convert schema (str) to dictionary

        json.loads(data) refuses identifies with single quotes.Use
        ast.literal_eval() instead.

        :param str schema: schema string
        :return str schema: schema as dictionary
        """
        try:
            schema = json.loads(schema)
        except Exception:
            schema = ast.literal_eval(schema)
        return schema

    def _search_display_name_full(self, operator, value):
        if value:
            builders = self.search([('title', operator, value)])
        if builders:
            return [('id', 'in', builders.ids)]
        else:
            return [('id', '=', False)]

    @api.onchange('formio_js_options_id')
    def _onchange_formio_js_options_id(self):
        if self.formio_js_options_id:
            self.formio_js_options = self.formio_js_options_id.value

    @api.onchange('wizard')
    def _onchange_wizard(self):
        if self.wizard:
            if self.schema:
                schema = self._decode_schema(self.schema)
                schema['display'] = "wizard"
                self.schema = json.dumps(schema)
            else:
                self.schema = '{"display": "wizard"}'
        else:
            if self.schema:
                schema = self._decode_schema(self.schema)
                del schema['display']
                self.schema = json.dumps(schema)

    @api.depends('formio_res_model_id')
    def _compute_res_model_id(self):
        for r in self:
            if r.formio_res_model_id:
                r.res_model_id = r.formio_res_model_id.ir_model_id.id
                r.res_model = r.formio_res_model_id.ir_model_id.model
            else:
                r.res_model_id = False
                r.res_model = False

    @api.depends('title', 'name', 'version', 'state')
    def _compute_display_fields(self):
        for r in self:
            r.display_state = get_field_selection_label(r, 'state')
            if self._context.get('display_name_title'):
                r.display_name_full = r.title
            else:
                r.display_name_full = _("{title} (state: {state}, version: {version})").format(
                    title=r.title, state=r.display_state, version=r.version)

    @api.depends('public')
    def _compute_public_url(self):
        for r in self:
            if r.public and request:
                url_root = request.httprequest.url_root
                self.public_url = '%s%s/%s' % (url_root, 'formio/public/form/new', r.uuid)
            else:
                r.public_url = False

    @api.depends('portal')
    def _compute_portal_urls(self):
        for r in self:
            if r.portal and request:
                url_root = request.httprequest.url_root
                r.portal_url = '%s%s/%s' % (url_root, 'my/formio/form/new', r.name)
            else:
                r.portal_url = False

    def _compute_languages(self):
        for r in self:
            languages = r.translations.mapped('lang_id')
            lang_en = self.env.ref('base.lang_en')
            if lang_en.active and r.language_en_enable and 'en_US' not in languages.mapped('code'):
                languages |= lang_en
            r.languages = languages.sorted('name')

    def _compute_edit_url(self):
        # sudo() is needed for regular users.
        for r in self:
            url = '{base_url}/formio/builder/{builder_id}'.format(
                base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
                builder_id=r.id)
            r.edit_url = url

    def _compute_act_window_url(self):
        for r in self:
            action = self.env.ref('formio.action_formio_builder')
            url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
                id=r.id,
                model=r._name,
                action=action.id)
            r.act_window_url = url

    def _compute_show_api_alert(self):
        self.ensure_one()
        self.show_api_alert = len(self.server_action_ids) > 0

    def _compute_api_alert(self):
        self.ensure_one()
        self.api_alert = ', '.join(self._api_alert_items())

    def _compute_debug_mode(self):
        for r in self:
            r.debug_mode = r.debug and request.session.debug

    def _api_alert_items(self):
        self.ensure_one()
        if len(self.server_action_ids) > 0:
            return [_("Server Actions")]
        else:
            return []

    def action_view_formio(self):
        # return {
        #     "type": "ir.actions.act_url",
        #     "url": self.edit_url,
        #     "target": "new"
        # }
        formio_view = self.env.ref('formio.view_formio_builder_formio')
        form_view = self.env.ref('formio.view_formio_builder_form')
        return {
            "name": self.display_name_full,
            "type": "ir.actions.act_window",
            "res_model": "formio.builder",
            "views": [(formio_view.id, 'formio_builder'), (form_view.id, 'form')],
            "view_mode": "formio_builder",
            "target": "current",
            "res_id": self.id,
            "context": {}
        }

    def action_view_forms(self):
        forms_view = self.env.ref('formio.view_formio_form_tree')
        return {
            'name': 'Forms',
            'type': 'ir.actions.act_window',
            'res_model': 'formio.form',
            'view_mode': 'tree,form',
            'views': [(forms_view.id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': [('builder_id', '=', self.id)],
            'context': {}
        }

    def _compute_forms_count(self):
        for r in self:
            r.forms_count = len(r.forms)

    def action_draft(self):
        vals = {'state': STATE_DRAFT}
        if self.is_locked:
            vals['is_locked'] = False
        self.write(vals)

    def action_current(self):
        self.ensure_one()
        self.write({'state': STATE_CURRENT, 'is_locked': True})

    def action_obsolete(self):
        self.ensure_one()
        self.write({'state': STATE_OBSOLETE})

    def action_lock(self):
        self.ensure_one()
        self.write({'is_locked': True})

    def action_unlock(self):
        self.ensure_one()
        self.write({'is_locked': False})

    @api.returns('self', lambda value: value)
    def copy_as_new_version(self):
        """Get last version for builder-forms by traversing-up on parent_id"""

        self.ensure_one()
        builder = self

        while builder.parent_id:
            builder = builder.parent_id
        builder = self.search([('name', '=', builder.name)], limit=1, order='id DESC')

        alter = {}
        alter["parent_id"] = self.id
        alter["state"] = STATE_DRAFT
        alter["version"] = builder.version + 1
        alter["version_comment"] = _('Write comment about version %s ...') % alter["version"]

        res = super(Builder, self).copy(alter)
        return res

    def action_new_builder_version(self):
        self.ensure_one()
        res = self.copy_as_new_version()

        form_view = self.env.ref('formio.view_formio_builder_form')
        tree_view = self.env.ref('formio.view_formio_builder_tree')

        return {
            "name": self.name,
            "type": "ir.actions.act_window",
            "res_model": "formio.builder",
            "view_type": "form",
            "view_mode": "form, tree",
            "views": [
                [form_view.id, "form"],
                [tree_view.id, "tree"],
            ],
            "target": "current",
            "res_id": res.id,
            "context": {}
        }

    def _get_js_options(self):
        """ formio.js (API) options """

        if self.formio_js_options:
            try:
                options = json.loads(self.formio_js_options)
            except Exception:
                options = ast.literal_eval(self.formio_js_options)
        else:
            options = {}

        options['i18n'] = self.i18n_translations()

        # language
        Lang = self.env['res.lang']
        if self.env.user.lang in self.languages.mapped('code'):
            language = Lang._formio_ietf_code(self.env.user.lang)
        else:
            language = Lang._formio_ietf_code(self._context['lang'])

        # only set language if exist in i18n translations
        if options['i18n'].get(language):
            options['language'] = language
        elif self.language_en_enable:
            lang_en = self.env.ref('base.lang_en')
            options['language'] = Lang._formio_ietf_code(lang_en.code)

        return options

    def _get_form_js_locales(self):
        locales = {lang.formio_ietf_code: lang.formio_short_code for lang in self.languages}
        return locales

    def _get_js_params(self):
        """ Odoo JS (Owl component) misc. params """
        params = {
            'cdn_base_url': self._cdn_base_url(),
            'portal_save_draft_done_url': self.portal_save_draft_done_url,
            'portal_submit_done_url': self.portal_submit_done_url,
            'readOnly': self.is_locked,
            'autoSave': self.auto_save,
            'wizard_on_change_page_save_draft': self.wizard and self.wizard_on_change_page_save_draft,
            'submission_url_add_query_params_from': self.submission_url_add_query_params_from,
        }
        return params

    @api.model
    def get_builder_uuid(self, uuid):
        """ Get builder by uuid or False. """

        domain = [
            ('uuid', '=', uuid),
        ]
        builder = self.sudo().search(domain, limit=1)
        if builder:
            return builder
        else:
            return False

    @api.model
    def get_portal_builder_uuid(self, uuid):
        """ Verifies portal access to forms and return builder or False. """

        domain = [
            ('uuid', '=', uuid),
            ('portal', '=', True),
        ]
        builder = self.sudo().search(domain, limit=1)
        if builder:
            return builder
        else:
            return False

    @api.model
    def get_portal_builder_name(self, name):
        """ Verifies portal access to forms and return builder or False. """

        domain = [
            ('name', '=', name),
            ('state', '=', STATE_CURRENT),
            ('portal', '=', True),
        ]
        builder = self.sudo().search(domain, limit=1)
        if builder:
            return builder
        else:
            return False

    def _get_portal_form_js_params(self):
        """ Odoo JS (Owl component) misc. params """
        params = {
            'cdn_base_url': self._cdn_base_url(),
            'portal_save_draft_done_url': self.portal_save_draft_done_url,
            'portal_submit_done_url': self.portal_submit_done_url,
            'scroll_into_view_selector': self.portal_scroll_into_view_selector,
            'wizard_on_change_page_save_draft': self.wizard and self.wizard_on_change_page_save_draft,
            'submission_url_add_query_params_from': self.submission_url_add_query_params_from,
        }
        return params

    def _get_public_form_js_params(self):
        """ Odoo JS (Owl component) misc. params """
        params = {
            'cdn_base_url': self._cdn_base_url(),
            'public_save_draft_done_url': self.public_save_draft_done_url,
            'public_submit_done_url': self.public_submit_done_url,
            'scroll_into_view_selector': self.public_scroll_into_view_selector,
            'wizard_on_change_page_save_draft': self.wizard and self.wizard_on_change_page_save_draft,
            'submission_url_add_query_params_from': self.submission_url_add_query_params_from,
        }
        return params

    @api.model
    def get_public_builder(self, uuid):
        """ Verifies public (e.g. website) access to forms and return builder or False. """

        domain = [
            ('uuid', '=', uuid),
            ('public', '=', True),
        ]
        builder = self.sudo().search(domain, limit=1)
        if builder:
            return builder
        else:
            return False

    @api.model
    def get_builder_by_name(self, name, state=STATE_CURRENT):
        """ Get the latest version of a builder by name. """

        domain = [
            ('name', '=', name),
            ('state', '=', state)
        ]
        builder = self.sudo().search(domain, limit=1)
        return builder or False

    def _cdn_base_url(self):
        Param = self.env['ir.config_parameter'].sudo()
        cdn_base_url = Param.get_param('formio.cdn_base_url')
        return cdn_base_url

    def i18n_translations(self):
        i18n = {}
        # formio.js translations
        for trans in self.formio_version_id.translation_ids:
            code = trans.lang_id.formio_ietf_code
            if code not in i18n:
                i18n[code] = {trans.source_property: trans.value}
            else:
                i18n[code][trans.source_property] = trans.value
        # Form Builder translations (labels etc).
        # These could override the former formio.js translations, but
        # that's how the Javascript API works.
        for trans in self.translations:
            code = trans.lang_id.formio_ietf_code
            if code not in i18n:
                if trans.source_property:
                    i18n[code] = {trans.source_property: trans.value}
                else:
                    i18n[code] = {trans.source: trans.value}
            else:
                if trans.source_property:
                    i18n[code][trans.source_property] = trans.value
                else:
                    i18n[code][trans.source] = trans.value
        return i18n

    def _formio_translate(self, source, lang_code=None):
        self.ensure_one()
        if not lang_code:
            lang_code = self.env.lang
        trans = self.translations.filtered(
            lambda t: t.lang_id.code == lang_code and t.source == source
        )
        return trans[0].value if trans else source

    def _etl_odoo_config(self, formio_form=None, params={}):
        return {}

    def _etl_odoo_data(self, formio_form=None, params={}):
        return {}

    def _generate_odoo_domain(self, domain=[], params={}):
        return domain

    def _has_extra_asset(self, extra_asset_record):
        return self.extra_asset_ids.filtered(lambda x: x.id == extra_asset_record.id)
