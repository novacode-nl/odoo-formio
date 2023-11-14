# Changelog

## 15.0.6.13

Hide field `builder_id_domain` in `formio.form` form view.

- Sidebar pabel disappears for long forms. This reverts some (resizing) changes from 16.0.7.0.
- Show the "Auto-save" setting in the dock before State.

## 15.0.6.12

Possibility to redirect the (parent) window upon submit of an embedded public form.

The redirect occurs if the `<iframe/>` has set:
- URL query-param `?embed` (any value allowed).
- Following `sandbox` attribute with values (AFAIK): `sandbox="allow-same-origin allow-scripts allow-top-navigation"`

## 15.0.6.11

Fix portal form `AttributeError: 'tuple' object has no attribute 'formio_ietf_code'`.\
Add (again) `language` template variable in the render values of endpoint `/formio/portal/form/<string:uuid>`\
Issue: [\#257](https://github.com/novacode-nl/odoo-formio/issues/257)

## 15.0.6.10

Rename label of `formio.form` field `submission_data`, from `Data` to `Submission Data`.

## 15.0.6.9

Add `formio.form` (Form) `after_save_draft` method and execute it in the `/submit` endpoints (backend, portal, public).

## 15.0.6.8

Fix:
Still one Form loading regression (bug) in template `formio_form_public_embed`.\
Due to incomplete implementation of the new (loading) spinner implementation in v16.0.6.6.

## 15.0.6.7

Fix:
Form loading on portal and public/website.\
Due to incomplete implementation of the new (loading) spinner implementation in v16.0.6.6.

Improvement:
Put the form builder (loading) spinner in dedicated `<div/>` which hides when the form builder has been rendered.

## 15.0.6.6

Improvements:
- Menu renaming: 'Forms' to 'Form Submissions'
- Put the form (loading) spinner in dedicated `<div/>` which hides when the form has been rendered.

## 15.0.16.5

Improvements:
- Menu renaming: 'Forms' to 'Form Submissions'
- Put the form (loading) spinner in dedicated `<div/>` which hides when the form has been rendered.

## 15.0.16.4

Security fix / meaurement:\
Deny update of `submission_data` (field) upon form update, if the form has state 'Completed' or 'Canceled'.

## 15.0.16.3

Improvement for translations:
- Add translate function in `formio.builder` model
- Set language (IETF code) in payload of `customValidation` hook.

## 15.0.16.2

In Form Builder form-view, add group "main" in top of the notebook/page "formio_components_api".

## 15.0.16.1

Fix standalone form (`formio.form`) record create, shouldn't set the `res_id`.\
This also results in a visible button to open the linked resource.

## 15.0.16.0

Changes:
- Implement the formio.js `customValidation` hook, which XHR posts to the API / validation endpoint.
- Some code reorder, cleanup and comments.

## 15.0.15.6

Add to Python eval context of `ir.actions.server` code:
- `_logger` - logger object
- `os.getenv` - get (os) environment variable function

## 15.0.15.5

Implement a `api=getData` model access-rights bypass, by obtaining a direct record rule (`ir.rule`).\
Provide the  record-rule (`ir.rule`) ID in the query-param `&module_rule_id=<model('ir.rule'):model_rule_id>`, shown in the example below.\
The domain of the record-rule applies and the model `search_read` shall be executed with superuser mode (`sudo()`).

Example URL (query params):
`http://localhost:8069/formio/portal/form/new/FORMIO_BUILDER_NAME?api=getData&model=stock.production.lot&label=name&model_rule_id=99`

## 15.0.15.4

Fix and improve 'datetime' component localization and translations:\
- Fix and improve `patchRequireLibrary` (JS function) to gradually determine the arguments.
- Fix and improve Form Builder `setLanguage` to localize datetime components.

## 15.0.15.3

Ensure external JavaScript libraries get loaded as expected by a common CDN.\
This introduces the `patchRequireLibrary` (JS function) which alters some library URLs the formio.js `CDN` class fetches.\
Currently the Flatpickr localizations URLs are altered.

## 15.0.15.2

### Improvement

Render a new portal form by the generic QWeb form template.\
This ensures to apply any extra form builder config/settings.

## 15.0.15.1

Backwards formio.js compatibility fix:\
Apply `patchCDN` if there's an instantiated `Formio.cdn` object.

## 15.0.15.0

Make formio.js CDN for hot-loaded dependencies configurable.

### Description

Make use of the formio.js CDN class to override the base URL for all 3rd party assets that are loaded on-the-fly by formio.js lib.\
This includes for example ACE, CKEditor, Flatpickr, Quill etc.

The Cloudflare CDN is set as the default value.\
They have a page about the GDPR: https://www.cloudflare.com/trust-hub/gdpr/

It's also possible to override the default value to a (paid) GDPR-aware CDN like KeyCDN.com or GlobalConnect.no and host the required files there,\
or simply point it to the base URL of their Odoo install and ship the files.\
This would require pinning the formio.js version, since different versions of the library need different dependencies.

## 15.0.14.2

### Fix

Fix migration for version 15.0.14.1 upgrade error:\
`UniqueViolation: duplicate key value violates unique constraint "ir_config_parameter_key_uniq"`

### Improvements

Style (highlight) active language button.

The "Forms" Button in the Form Builder view.

Archive functionality for formio.js versions (also unarchive and search filter).

Wizard draft autosave mode.\
This allows complex components to serialize their data on the form before submitting it.

## 15.0.14.1

Improve app/module installation, by downloading and installing a default formio.js library version after install.\
Also log a warning in case an error (eg ConnectionError) occurs.

## 15.0.14.0

### Refactored the Form its Form Builder (field) domain/filter.

This solves the deprecation warning, regarding a domain that may not be returned by an onchange method.

Replace the `_onchange_builder_id` method (implementation), by a new computed field `builder_id_domain` and 2 new methods:
- `_compute_builder_domain`
- `_get_builder_domain`.

This also affects the implementation replacement in additional modules which should be updated as well !\
Eg: `formio_crm`, `formio_partner`, `formio_purchase`, `formio_sale`.

**WARNING / UPDATE REQUIREMENT**

Update all modules which implemented the `_onchange_builder_id` method.\
For the (Nova Code) Forms modules those are:
- formio_crm
- formio_partner
- formio_purchase
- formio_sale

### Add new feature which allows Form Builders in "Draft" or "Obsolete" state to be choosen in a new Form in the backend.

The 2 setting fields are available in the Form Builder:
- Use Draft in Backend
- Use Obsolete in Backend

## 15.0.13.7

In the Form Builder, implement conditional warning (also extendable) in case there are integrated APIs.\
This warns the Form Builder user about components being removed or updated, which could lead the API regression/breakage.

## 15.0.13.6

- Fix language determination (cascade) for public Form load by UUID.
- Add cascade delete on `formio_version_id` in model `formio.version.translation`.

## 15.0.13.5

Update iframe-resizer v4.3.6 (JS library).

## 15.0.13.4

Add form/builder heightCalculationMethod 'taggedElement' targets in portal and public templates.

## 15.0.13.3

Change form 'heightCalculationMethod' from 'grow' to 'taggedElement'.\
This solves issues for components with dynamic height, eg the collapsible Edit Grid (type `editgrid`).

## 15.0.13.2

Fix formio.js version (action/button) _Download and install_ error:\
`ValueError: max() arg is an empty sequence`.\
Initialize the translations sequence properly.

## 15.0.13.1

Improvements for Version Translations (model: `formio.version.translation`):
- Compute and store origin (base translation, user added).
- Compute and show whether a copied (origin) base translation has been updated.
- Add sequence field. So translations can be ordered to ease admnistration and the translation override implementation.

Fix `name_get` method (models: `formio.translation`, `formio.version.translation`)

## 15.0.13.0

Major improvements for translations:
- Specific Version Translations instead of linking (Many2many) to the available Base Translations.
- Translations (overrides) of formio.js source properties in the form builder.

Add `noupdate=1` for the xmlid `formio.version_dummy` data (record).\
This prevents recreation when the dummy version has been archived (is inactive).

## 15.0.12.12

Fix the component data URL check in the Form JS (rendering) code.

## 15.0.12.11

Improve loading "Extra Assets" (js, css), by targetting `before` or `after` the core assets.

## 15.0.12.10

Form Builder: Disallow create and edit for field "formio.js version".

## 15.0.12.9

Form Builder Lock/Unlock buttons with primary color.

## 15.0.12.8
Cleanup/fix migrations (apparently picked from 16.0)

## 15.0.12.7

Improve Form Builder "Actions API" tab (layout and info).

## 15.0.12.6

Improvements for administration of "Extra Assets" (js, css) with link/relation to attachments.\
Affected models: `formio.extra.asset`, `ir.attachment`.

## 15.0.12.5

Implement "Forms Ref" field on several models regarding assets and attachments:\
`formio.version.asset`, `formio.extra.asset`, `ir.attachment`\
This facilitates purposes like export/import tools.

## 15.0.12.4

Improve form builder wizard save as draft: previous page, page clicked.

## 15.0.12.3

Fix `formio.builder` typo in `_constaint_check_name`.

## 15.0.12.2

Fix and improve email templates:
- Migrate Jinja to QWeb syntax.
- Replace `email_to` by `partner_to`.

## 15.0.12.1

Add unique constraint on `formio.builder.translation` (fields: `builder_id`, `lang_id`, `source`).

## 15.0.12.0

This release brings datetime component localization and translations:
- Add `formio.extra.asset` (model, views) to store extra JS and CSS assets, eg `flatpickr` (JS library) and its localization files.
- Implement locales administration and passing to the (JS) frontend.
- Set default and update the datetime (flatpickr) locale by language chooser in a form.

## 15.0.11.11

Fix typo menu (sequence).

## 15.0.11.10

Menu: put Form Builders first.

## 15.0.11.9

Field "Forms Ref" (`formio_ref`) is required in Server Action (view) when Model is a Form (`formio.form`).

## 15.0.11.8

Add field "Forms Ref" (`formio_ref`) in Server Actions list view.

## 15.0.11.7

Rename field `formio_code` to `formio_ref`.\
It has more meaning and cannot be confused with coding.

## 15.0.11.6

Enable loading the config (eg options) of Forms using the backend `_etl_odoo_config` method:
- Add form builder method `_etl_odoo_config`.
- Extend controllers `/config` (http) endpoints with updating the config by `_etl_odoo_config`.
- Change the (JavaScript) `loadForm` method, to obtain and add possible URL query string/params from the window or parent window.

## 15.0.11.5

Provide an informational reference (link) between Form Builder and Server Actions:
- Form Builder (form view): new tab "Actions API" where server actions can be linked.
- Add char field "Forms Code" in server action (form view).

## 15.0.11.4

- Ensure users with (group) "Administration Settings" are assigned to the "Forms Administrator" group.

## 15.0.11.3

- Improve Form (iFrame) resizing, especially for wizard Forms.\
  Ensure iFrame height shall be recomputed in wizard Forms upon next/prev page.\
- Revert the `heightCalculationMethod` from `lowestElement` to `grow` again.\
  The `lowestElement` added too much space at the bottom (stil no clue why that happens).

## 15.0.11.2

Improve Form (iFrame) resizing, especially for wizard Forms.\
Change the `heightCalculationMethod` from `grow` to `lowestElement`.\
This resizes upon every (component) change by obtaining the lowest bottom element.

## 15.0.11.1

Solve Form height resizing issues, by applying the iFrame Resizer `bodyMargin` option.\
Eg. ensure the rendering of select component at the bottom of a Form won't break anymore.\
Issue: [\#20](https://github.com/novacode-nl/odoo-formio/issues/20)

- Update iFrame Resizer (JS) library to version 4.3.2 (Dec 2021).
- Add configurable `iframe_resizer_body_margin` field in Form Builder, with a (sensible) default value.
- Change Form templates (backend, portal) to apply the configurable iFrame Resizer `bodyMargin`.
- Add callable template `formio.form_iframe` (with options: `src`, `bodyMargin`, `form`), which applies the iFrame Resizer (with fallback on `form` its Form Builder).

## 15.0.11.0

- Add Form (JS) `apiUrl` property (backend, portal, public).
- Implement Form (JS) `change` event, which posts to `/api/onChange` endpoint (determined by `apiUrl`).

## 15.0.10.7

Implement missing `api=getData` (fetching) endpoints in backend, portal, public.

## 15.0.10.6

Add default Form Builder formio.js Options data.

This contains an `editForm` configuration for the `select` component.\
More info about the `overrideEditForm` property: https://github.com/formio/formio.js/issues/2280

However the `dataSrc` property currently (December 2022) doesn't seem to work, also mentoined in: https://github.com/formio/formio.js/issues/2489

## 15.0.10.5

Rename `/data` (fetching) endpoints query param from `api=get_data` to `api=getData`.

## 15.0.10.4

- Moved transalations button after form builder.

## 15.0.10.3

- For clarity (between code and Components API), renamed field added in 10.1:\
  from `submission_url_add_query_string` to `submission_url_add_query_params_from`.

## 15.0.10.2

Refactor (and deprecate) the `/data` (fetching) endpoints to form root-level endpoints by new query string `api=get_data`.\
Unfortunately this is required to allow the query string feature added in 10.1 to use with the data endpoint as well.

## 15.0.10.1

Fundamentals to implement prepopulation* of component values for new (portal, public) forms.\
Prepopulation* by means of the Components (server) API.
- Form Builder configuration and frontend/JS: add possible URL query string from window, to submission URL.
- New (portal) endpoint: `/formio/portal/form/new/<string:builder_uuid>/submission`\
  Can be used to prepopulate a (new) form.

## 15.0.10.0

- Portal form: render new (not yet stored) or a direct create (old style)
- Refactor `_generate_odoo_domain`.

## 15.0.9.28

- Extend the form `/data` endpoints to support advanced domain filter.
- Add the basic `_generate_odoo_domain` function in `formio.form` model, used in form `/data` endpoint.

## 15.0.9.27

- Don't copy the Form Builder Locked field.

## 15.0.9.26

- Improve the "Redirect After Submit" feature, to also support when the form is in the same window (not only iframe).

## 15.0.9.25

- Form Builder: Copy the Translations upon Create New Version\
  Issue: [\#139](https://github.com/novacode-nl/odoo-formio/issues/139)\
  PR: [\#190](https://github.com/novacode-nl/odoo-formio/pull/192)

## 15.0.9.24

- Fix Dummy version info in Builder.
- Archive Dummy version upon install of a real version.

## 15.0.9.23

- Builder: formio.js version (field) domain/filter exclude Dummy.
- Builder: hide the Assigned user (`user_id`) field.\
  Let's see if this still needed, otherwise change to `Many2many`.
- Remove menu to `formio.res.model`\
  Issue: [\#190](https://github.com/novacode-nl/odoo-formio/issues/190)

## 15.0.9.22

- Remove `formio.version` and related assets data
- Add Dummy `formio.version` record (without assets)
- Add Dummy `formio.version` to `formio.builder` Demo data
- Show warning about Dummy version `formio.builder` form view.

## 15.0.9.21

- Fix language determination in public Form.\
  Derive in order: context, user, base.lang_en.

## 15.0.9.20

- Dutch (nl_NL) translations improvements.

## 15.0.9.19

- Form Builder set to "Draft" state now unlocks too.\
  Code change: `action_draft` now updates `is_locked=False`, if `is_locked`.

## 15.0.9.18

- Minor change: name (attr) on 2 view groups `portal_redirect_after_submit`, `public_redirect_after_submit`

## 15.0.9.17

- Fix completed wizard form, with "Save draft on next page" (setting).\
  When navigating pages, the form state has been updated from "complete" to "draft".\
  Issue: [\#184](https://github.com/novacode-nl/odoo-formio/issues/184)

## 15.0.9.16

- Remove searchbar from Builder and Form.

## 15.0.9.15

- Set the (form) language in the fetch `/data` URL.

## 15.0.9.14

- Upon copy `formio.version` record, also copy the (One2many) assets.

## 15.0.9.13

- Fix backend submit-URL (endpoint) of Form in Wizard-mode, when Form Builder enables the "Wizard on next Page Save Draft".\
  This concerns (fixes) changes in versions, 9.8, 8.32.

## 15.0.9.12

- Form Builder: unlock/lock feature, allows to modify a published Form Builder (in state: Current).

## 15.0.9.11

- Improve `formio.form` its `_compute_access` method, to allow root user (`self.env.su`).

## 15.0.9.10

- Layout improvements in Builder and Form (backend form) views.
- Fix duplicate field label warnings for model `formio.builder.translation`.

## 15.0.9.9

- Store related fields in model `formio.builder.translation`, to enable sorting.

## 15.0.9.8

- Fix submit-URL of Form in Wizard-mode for backend auth-mode, when Form Builder enables the "Wizard on next Page Save Draft".\
  This concerns the feature added in version 8.32.
- Upon submit `/formio/public/form/create/<builder_uuid>/submit` set the Form (record) field `public_share=True`.\
  This allows an internal user to use (eg test) such public Form as well, with identical public (share expiration) functionality.

## 15.0.9.7

- Public existing (eg invited) form: Redirect submit-done URL feature.\
  Similar feature already available with public created (website) and portal Forms.

## 15.0.9.6

- Form Builder: Translations button with action window.\
  Ease the editting, export/import of Form Builder Translations.

## 15.0.9.5

- Public (website): Fix JavaScript (frontend) to set the proper `/data` URL-path on component objects, which fetch (Odoo) model records.

## 15.0.9.4

- Portal: Fix `/data` URL-path to fetch (Odoo) model records.\
  This required to change the Form URL in (embed) iframe:\
  - from: `/formio/form/<string:uuid>?portal=true`\
  - to: `/formio/portal/form/<string:uuid>`
- Public (website): Implemented feature `/data` URL-path, to fetch (Odoo) model records.\
  This configuration requires additional model read-access for the public user, on the model to fetch the records from.

## 15.0.9.3

- Improve the formio.js library Downloader and Installer tool.\
  Fetch 100 tags by adding (URL query) parameter `per_page=100`.\
  Previously, 30 tags were fetched (default `per_page=30`).

## 15.0.9.2

- Fix Form submit: Error `_logger is undefined` in method `mail_activity_partner_linking`.\
  Affected feature: Components API (tab in Builder) Partner

## 15.0.9.1

- Fix Form Builder: Access Error (read) `ir.ui.view` upon action "Create New Version".\
  This now correctly determines the views (form, tree) by xmlid.

## 15.0.9.0

- Improve the formio.js library Downloader and Installer tool.\
  Downloads and installs belong and go in the `ir.attachment` model and filestore which ensures proper permissions.\
  Previous implementation located these into the `formio` module its `static/installed` directory.

## 15.0.8.34

- Fix settings view (res.config.settings). Some settings and info appeared while searching for other settings.
  Issue: [\#164](https://github.com/novacode-nl/odoo-formio/issues/164)

## 15.0.8.33

- Fix warning: `Two fields (formio_version_name, formio_version_id) of formio.builder() have the same label.`
- Fix warning: `The domain term '('formio_version_id', '=', [py:int])' should use the 'in' or 'not in' operator.`

## 15.0.8.32

- New feature for public Form in Wizard mode: on next page perform a save draft.\
  This is a (boolean/checkbox) setting in the Builder.

## 15.0.8.31

- Add *formio.js* (library project) license file, also with GitHub downloader/installer.\
  *formio.js* - https://github.com/formio/formio.js

## 15.0.8.30

- Improve the submitDone redirect feature.\
  Config should be explicit; don't wait on timeout and then redirect anymore.

## 15.0.8.29

- Add session variable `formio_last_form_uuid` upon POST `/formio/public/form/create`.

## 15.0.8.28

- Correct misunderstanding, leftover names regarding the formio.js library.

## 15.0.8.27

- Fix bug/regression in `formio.form` (create) `_prepare_create_vals` and `write`, due to timezone feature added in version 8.25

## 15.0.8.26

- Fix bug/regression in `formio.form` (create) `_prepare_create_vals`, due to timezone feature added in version 8.25

## 15.0.8.25

- Store timezone (from the partner) of the Form submission.

## 15.0.8.24

- Add translation for the alert message(s), in top of the Form.
  - Translated for language codes: nl, nl_BE, pt_BR, zh_CN.
  - Relates to: https://github.com/formio/formio.js/issues/3105, https://github.com/formio/formio.js/issues/2627
- Add translation for the submitError message, near submit button of the Form.
  - Translated for language codes: nl, nl_BE, pt_BR, zh_CN.

## 15.0.8.23

- Fix: Nested components (eg inside datagrid, editgrid) **Data Source URL**
- Prefix the Data Source URL with the Odoo controller endpoint, with format: `/formio/form/<string:uuid>/data/?query...`

## 15.0.8.22

- Fix: Language determination in Public Form (also used by the `website_formio` module).
- Improve JsonRPC client using Odoo's JsonRpc internals (from `web.ajax`).

## 15.0.8.21

- Form Builder (UI) improvement: Extend width to 95% of container (viewport), which was too narrow before.

## 15.0.8.20

- Fix: Ordering of "formio.js version" in (Many2one) selection fields e.g. in Form and Config settings.

## 15.0.8.19

- Fix: Translations didn't worked, due to regression by latest change in `formio.builder` function `i18n_translations`

## 15.0.8.18

- Fix: Issue in Form (form-view) searching Builder(s) really didn't worked properly.\
  Technical details:\
  This change addresses the `formio.builder`, adding the `search` method for the computed field `display_name_full` which is used as `_rec_name`.

## 15.0.8.17

- Fix: Error when uninstall and installing again. `Record does not exist or has been deleted. (Record: formio.builder.js.options(1,), User: 2)`\
  Uninstall now deletes the system parameter (record) with key `formio.default_builder_js_options_id`

## 15.0.8.16

- New feature: Grant copy Forms persmission (button), also in portal, configured by Form Builder.\
  It's also possible to configure whether the Form should be copied and merged into the latest/current Form Builder schema (design).

## 15.0.8.15

- Removed rigorous record rule `ir_attachment_unlink_formio_form` (Attachments of completed Forms can't be deleted).\
  This was intended, now moved and improved in the module `formio_storage_filestore`.

## 15.0.8.14

- Fix: delete and cancel actions of Form in the portal.

## 15.0.8.13

- Forms app/module Category.
- In User form, ensure User Groups in dropdown/select instead of checkboxes.

## 15.0.8.12

- Form (field) Title is required and indexed.

## 15.0.8.11

- Fix singleton error, when matching multiple Partners by email in the Form (e.g. for following and report emails).\
  PR: [\#109](https://github.com/novacode-nl/odoo-formio/pull/109)
- Schedule Activity (on Form) if found multiple Partners with same email submitted in the Form.

## 15.0.8.10

- JavaScript: Set the `baseUrl` (value: `window.location.href`) on the (formio.js) Formio object.\
  The `baseUrl` is the Form it's `<iframe src=.../>` attribute.\
  This can be used in other (integration) modules e.g. for security/access checking etc.

## 15.0.8.9

- Fix server crashing due to request unbound error, while installing or updating module.\
  Bug has been introduced in version 8.7, `formio.builder` function `_compute_public_url` of computed field `public_url`.

## 15.0.8.8

- In model `ir.attachment` define the relational field `formio_form_id = fields.Many2one('formio.form')`\
  Can be used for all kinds of integration e.g. files upload storage.

## 15.0.8.7

- In Form Builder show URL/link to public create Form (e.g. to embed, share).

## 15.0.8.6

- Fix: Language determination in Public Form (also used by `website_formio` module).\
  PR: [\#101](https://github.com/novacode-nl/odoo-formio/pull/101)

## 15.0.8.5

- Fix (4): language switcher buttons and translations in public Forms (also used by `website_formio` module).\
  Convert the Odoo language code (underscore "_") to Formio (formio.js) JavaScript's i18n expected IETF code (hyphen "-").\
  PR: [\#100](https://github.com/novacode-nl/odoo-formio/pull/100)

## 15.0.8.4

- Fix: formio.js version updates in Windows environments are not available.\
  PR: [\#92](https://github.com/novacode-nl/odoo-formio/pull/92)

## 15.0.8.3

- Fix (3): language switcher buttons and translations in Form Builder and Forms.\
  Convert the Odoo language code (underscore "_") to Formio (formio.js) JavaScript's i18n expected IETF code (hyphen "-").\
  Issues: [\#91](https://github.com/novacode-nl/odoo-formio/issues/91), [\#93](https://github.com/novacode-nl/odoo-formio/issues/93), [\#95](https://github.com/novacode-nl/odoo-formio/issues/95)

## 15.0.8.2

- Fix (2): language switcher buttons and translations in Form Builder and Forms.\
  Issues: [\#91](https://github.com/novacode-nl/odoo-formio/issues/91), [\#93](https://github.com/novacode-nl/odoo-formio/issues/93)

## 15.0.8.1

- Fix (1): language switcher buttons in Form Builder and Forms.\
  Shown languages (buttons) are determined by configured languages in the Form Builder.\
  Issues: [\#91](https://github.com/novacode-nl/odoo-formio/issues/91), [\#93](https://github.com/novacode-nl/odoo-formio/issues/93)
- Add translations pt_BR: Portuguese (BR)

## 15.0.8.0

- Rename the App and other UI parts (titles, labels) to "Forms"

## 15.0.7.9

- Fix: obtaining the latest GitHub 30 release versions often get (HTTP) 403 errors.\
  Adds a **GitHub personal access token** in the Settings, to get a higher rate limit.

## 15.0.7.8

- Fix: Forms should be accessible when user belongs to both groups: *User: Assigned forms* and *User: All forms*
  Group *User: All forms* takes precedence over *User: Assigned forms*.

## 15.0.7.7

- Translatable (multilingual) public Forms, with language-switcher buttons.\
  This addresses issues: [\#58](https://github.com/novacode-nl/odoo-formio/issues/58), [\#47](https://github.com/novacode-nl/odoo-formio/issues/47)
- Translatable (multilingual) Form Builder, with language-switcher buttons.

## 15.0.7.6

- New feature: specify Form Builder Javascript options API/argument.\
  Form Builder JavaScript options can be specified in the form-view (tab) and shall be stored in `formio.builder` record.\
  Default (global) JavasScript options can be specified in the Forms Settings, which are by default loaded while creating a Form Builder.\
  For example, the Form Builder editForm File component options: https://github.com/formio/formio.js/tree/master/src/components/file/editForm

## 15.0.7.5

- Fix Form Builder save (JavaScript event handler).\
  Use the event handler its argument (schema/components) instead of `self.schema` (scary change/bug)\
  Issue: [\#66](https://github.com/novacode-nl/odoo-formio/issues/66)

## 15.0.7.4

- Implemented Form Builder `copy()` method, which previously was blocked / not possible. This due to unique contraint validation on fields `name` and `version`.\
  Upon copy, the new Form Builder its name (field value) shall be suffixed with a datetime-stamp.

## 15.0.7.3

- Configurable redirect, after (submit) submission of Portal and Public (website) Form:
  - Configuration in Form Builder
  - Handle whether to redirect or reload (new) Form.
- Redirect after Submit-done configuration for Portal and Public (website) Forms.

## 15.0.7.2

- Fix Form not loaded. Javascript workaround (known) browser incompatibility errors.
  - Mac: Safari 12.x, 13.1
  - iOS: Safari\
  Issues:
  - Safari 13.1 on Mac experienced error: 1unexpected token '='. expected an opening '(' before a method's parameter list`
  - iOS issue solved, but details not debugged. Dev Tools not ready/present in iOS browsers.

## 15.0.7.1

- Fix frontend JavaScript: Execute `loadForm()` after the DOM has been `mounted()`, not upon (async) `willStart()`.\
  (This of course failed to bootstrap the (formio) App when the DOM wasn't loaded, which results in nothing).
- Improve frontend JavaScript: Add `initForm()` hook and implement specific constructor/object properties in the App classes (backend_app.js, public_app.js, public_create_app.js).\
  E.g. to set `config_url = '/formio/public/form/' + this.form_uuid + '/config';`

## 15.0.7.0
- Frontend rebuild with **Owl (Odoo Javascript framework)** - Form Builder and Form:
  - Use the Owl - https://odoo.github.io/owl - JavaScript framework, to abstract the Form component into a Component class.
  - JavaScript modules (export/import) to bind the Owl classes into specific backend and public Form (Owl) Apps.
  - This also breaks/ends support for Internet Explorer, which is already published EOL.
- Changed some endpoint URLs (to improve URL conventions).

## 15.0.6.1

- Version GitHub tags: Add scheduled action (ir.cron daily) which checks and registers new client/library Versions (GitHub tags).
- Version GitHub tags: Add field "Installed on", which stores the installation datetime.
- Version GitHub tags: Highlight installed version records with color (success/green).

## 15.0.6.0

- New feature: formio.js (client/library) Version Checker, Importer and Installer tool.\
  Now administrators can check, import (from GitHub) and install new releases/versions by a single click in Odoo.\
  Soon a scheduled Cron action shall be implemeneted which does the (default daily) checking and importing.
- New feature: Configuration setting to specify the default formio.js (client/library) Version for any new Form Builder.

## 15.0.5.3

- New Components API feature: create a Partner after Form submission. Possibility to add the Partner to Followers of the Form record.
  Configuration in Form Builder: Partner field/component (email, name), Add to Followers (checkbox/boolean).

## 15.0.5.2

- Add Form Builder UUID (field).
- Data migration: update all `formio_builder` records, set UUID (field) with generated value.
- Change the public Form loading and submit (URLs, handling) from ID to UUID.\
  This slightly protects from abuse of public Forms (some obfuscation of the real id).
  Issue: [\#46](https://github.com/novacode-nl/odoo-formio/issues/46)

## 15.0.5.1

- New tab *Components API* in Form Builder form-view.

## 15.0.5.0

- Public Forms - Access configuration and check (by interval expiration settings: minutes, hours, days).
- Public Forms - Improvements in (web)controller, templating and JavaScript:
  - Split up JavaScript files, which implement the Form handling (backend, public, public new).
  - This change is subjected to redundant code (DRY), but works for now and shall be addressed by using a JavaScript framework (probably Owl).
- Change `formio.form` toplevel URLs: remove the `/root` suffix.\
  This was introduced in 1.8. Seems not to be an issue anymore.

## 15.0.4.5

- Add optional UUID (field) into Forms list view.

## 15.0.4.4

- Change 4.3 implementation (`>final_res` fields), which was rather confusing:
  - Remove the `final_res_model`, `final_res_id` fields.
  - Instead: in model `formio.form` added fields `initial_res_model_id`, `initial_res_id`.
  - These fields store the initial (referenced) resource record. So swapping the `res_model_id` and `res_id` afterwards is supported, for specific implementation requirements.
  - Add migration to update `formio_form` records: `res_model_id` (determined by `formio_builder`), copy `res_id` to `initial_res_id`.

## 15.0.4.3

- In model `formio.form` added fields `final_res_model`, `final_res_id`.\
  These fields can be used to swap the (referenced) resource record, for specific implementation requirements.
- In model `formio.builder` added field `res_model`, which represents the technical model-name.

## 15.0.4.2

- In the **create Form (form-view)** by default provide only Form Builders **without Resource-model** in the **Form Builder drop-down field**.\
  Specific modules extend this (domain) filter to add appropriate Form Builders related to the (active) Resource-model - e.g. formio_sale, formio_stock.

## 15.0.4.1

- Improvement: ETL Odoo (resource) data into Form, requires to bypass access control on the target/resource model. (Use `sudo` here).

## 15.0.4.0

- Basic setup to deploy/share **public Forms**, by a setting (checkbox) in Form Builder.
- Implement **sequence field** in **Form**. Usefull when storing and listing forms in an ordered way.
- New setting (in Form Builder) which instructs the **Form** whether to **show/hide** the **UUID** in Form footer.
- **Store** those **show/hide** setting fields in the **Form**, instead of joining its relational Builder value (in readonly mode).
- **Improvements in tree/list and form views** regarding Form and Builder.

## 15.0.3.7

- New setting (in Form Builder) which instructs the Form whether to **show/hide** the **Title**.
- Moved the Form Title from the main HTML-document into the embedded document (iframe).\
  This improves the embedded Form experience.

## 15.0.3.6
- New settings (in Form Builder) which instructs the Form whether to **show/hide** some metadata: **Assigned user, Submission user &amp; date, ID, State**.\
  The default is to show all these metadata fields (for backwards compatibility and no data migration needed).
- Import formio.js version 3.x assets and bootstrap (CSS) instead of CDN.
- Fix silly Javascript bug: `_.extend` (underscore.js ain't loaded here). Use jQuery extend.
- Add help text regarding issue with (formio.js) and `view_as_html` setting https://github.com/formio/formio.js/issues/1545

## 15.0.3.5

- Add formio.js **v4.9.26** assets `https://github.com/formio/formio.js/releases/tag/v4.9.26`
- User in group *"Forms Admin"* can edit the Form it's submission data, for a new Form (if ain't stored).

## 15.0.3.4

- Don't override provided vals in `formio.form` function `_prepare_create_vals()`.

## 15.0.3.3

- New feature: ETL Odoo (resource) data into Form.\
  Supported fields:
  - Scalar fields e.g. Char, Text, Integer, Boolean, Date, Datetime
  - Many2one field (load it's leaf/scalar field)
  - One2many field, supported by formio.js Datagrid component

## 15.0.3.2

- Optional configuration to allow specific User Group(s) to force update of a **Form state** field (draft, complete, cancel) e.g. by buttons.\
  Feature/issue: [\#36](https://github.com/novacode-nl/odoo-formio/issues/36)

## 15.0.3.1

- Fix portal iframe (height) resizing issue [\#35](https://github.com/novacode-nl/odoo-formio/issues/35)

## 15.0.3.0

- Changed the way **Resource Fields** are determined and stored. Not by dependent/computed fields anymore, which caused all kind of troubles.\
  Affected fields: `res_name`, `res_info`, `res_act_window_url` and `res_partner_id`.\
  **!! CAUTION, BEFORE UPGRADE: Test first and be sure all Forms data (regarding these fields) has been migrated properly.**

## 15.0.2.3

- Form Builder layout improvements: full width, remove horizontal scrollbar.

## 15.0.2.2

- Fix (workaround) to solve form height-resizing issues [\#20](https://github.com/novacode-nl/odoo-formio/issues/20)

## 15.0.2.1

- Add formio.js **v4.9.23** assets `(https://github.com/formio/formio.js/releases/tag/v4.9.23)`
- Remove formio.js "latest" version (CDN URLs). Requests from CDN caused time-outs.

## 15.0.2.0

- Odoo formio **view types** for Builder and Form. Finally one can switch view types (form, formio) within the window action.
- Moved the so-called *Form dock* (info bar) into the iframe. This updates the info on a (iframe) window reload.
- Remove the *submit done url* implementation, which is useless in a backend usage/context.
- Other improvements and simplification.

## 15.0.1.10

- Extend `formio.form create` methods with `_prepare_create_vals` method, which in turn specific modules could call to assign field `vals`.
- Fix method `compute_res_fields` which stores fields regarding the resource model (made possible by change in former point).

## 15.0.1.9

- Computed fields regarding resource model: Store res_name and res_partner_id. Change dependent compute method.
- Add (related) field submission partner.

## 15.0.1.8

- Change URLs and controllers FROM `/formio/form/<action>/<string:uuid>` URLs TO `/formio/form/<string:uuid>/<action>`.\
  This solves issues regarding relative URLs from a Javascript perspective (components). The UUID was stripped by the Javascript client lib.\
  Should solve: [\#11](https://github.com/novacode-nl/odoo-formio/issues/11)
- Remove 2 legacy (obsolete) controller methods for routes: `/formio/form/<string:uuid>` and `/formio/builder/<int:builder_id>`

## 15.0.1.7

- Prevent Javascript clashes between Odoo and formio.js. Hence remove all Odoo Javascript (assets) loading in the formio.js iframe.
- Add and load standalone JsonRPC client.

## 15.0.1.6

- Portal: Improved (refactored) controller layout values method.
- Portal: form buttons now keep query-params.

## 15.0.1.5

- Demo Builder: Save as Draft (button).
- Form update to **Draft** fix (workaround). Remove `submission_data['submit']`.

## 15.0.1.4

- Include and serve the formio.js library assets (JS, CSS) within the module. Don't use CDN anymore.
- Click button to display the **Form Builder** in **Full Screen**.

## 15.0.1.3

- Portal: Improved (refactored) controller layout values method.
- Portal: form buttons now keep query-params.

## 15.0.1.2

- Rename (consistency) Builder form-view id/ref: from `view_formio_builder` to `view_formio_builder_form`.

## 15.0.1.1

- Possible "Resource model(s)" needs to be registered from sub-modules e.g. formio_sale.\
  Just choosing from all models is useless and confuses the user about its functionality.

## 15.0.1.0

- Form embedded in iframe. This avoids clashes (Javascript and CSS) between Odoo and formio.js.
- Redesign of templates

## 15.0.0.16

- Search filters on Form Builder and Forms.
- Assign a user (owner/author/designer) to a Form Builder.

## 15.0.0.15

- Change default forms view to list.
- Improve forms kanban to group by state.

## 15.0.0.14

- Form Builder versioning. Also create a new Builder version-record (from existing one).

## 15.0.0.13

- Form Builder states: Draft (in design), Current (published) and Obsolete (unpublished).

## 15.0.0.12

- Redesign of Builder and Form templates. A simplification and improvement.
- Hopefully fixed enough styling issues due to Bootstrap 4 VS 3 in Odoo and loaded JS Form (Builder).
- Other small improvements

## 15.0.0.11

- Include new formio.js versions and assets (3.27.3, 4.0.8)
- Add recommendation into the description of the "latest" formio.js version.

## 15.0.0.10

- Translation system for Form labels, placeholders etc.
- Language selector on Form.

## 15.0.0.9

- Simple Form wizard (is a Form rendering/display mode).

## 15.0.0.8

- Access-check improvements.
- UI improvements.
- Dutch translations.

## 15.0.0.7

- Dropdown button in Portal, to add and fill-in new Form(s).

## 15.0.0.6

- Form state (Pending, In Progress, Complete, Canceled).
- Form is readonly if state is Complete or Canceled.

## 15.0.0.5

- Form invitation mail.
- Improvements regarding form assignment (user filter).

## 15.0.0.4

- Portal User can use forms.
- Restrict access to assigned forms (Portal User, Internal User).

## 15.0.0.3

- Translations system to manage the translatable terms and load into the form.

## 15.0.0.2

- formio.js (library: JS, CSS) version management and loading.

## 15.0.0.1

Initial version.
