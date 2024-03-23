# Changelog

## 16.0.11.18

In the Form Builder, show a "Locked" badge in case it is locked.

## 16.0.11.17

- Fix crashing forms due to 16.0.11.16 (Scroll Into View).
- Improvements for Scroll Into View feature.
- Backwards compatibilty fix for (component) onChange event.

## 16.0.11.16

Add configurable automatic scrolling, especially useful in long-page wizard forms after switching previous/next page.\
This scrolls an element (CSS selector) into the visible area of the browser window.\
The element (CSS selector) can be set in the Form Builder for portal and public forms.

## 16.0.10.15

Fix form `formio.form` create, to set `public_share` by its `formio.builder``public` field.
This is still done (but not harmful) by `_onchange_builder` which needs to be fixed or removed.

## 16.0.10.14

Fix `ir.actions.server` model `_constraint_unique_formio_ref` method:\
`ValueError: Expected singleton: ir.actions.server`

## 16.0.10.13

Fix Form Builder with Autosave disabled to show the Save Form button when moving (ordering) components.

## 16.0.10.12

Improve the form (component) onChange API to apply Form options described in:\
https://help.form.io/developers/form-development/form-renderer#form-renderer-options

## 16.0.10.11

Fix public `/formio/public/form/<form_uuid>/config` endpoint.\
Pass the `formio.form` model object to methods `_etl_odoo_config()` and `_etl_odoo_data`.

## 16.0.10.10

In Form Builder, when Autosave is disabled, highlight a colored border when a manual saving is required.

## 16.0.10.9

Workaround for Safari 16.6 (AFAIK), with Columns in a Data Grid.\
The Columns become too narrow and unusable in a Data Grid.
GitHub issue: https://github.com/formio/formio.js/issues/5426

This workaround adds 1 CSS rule, which adds a `width: 100%` to the
first `<td/>` (column) targeted in a Data Grid table.

```css
#formio_form_app table.datagrid-table tbody tr td:first-child {
    width: 100%;
}
```

## 16.0.10.8

Fix form component "change" and "blur" (JS) APIs.\
An overlay was always expected, but it is not enabled by default, resulting in no API execution!

## 16.0.10.7

Update system parameter `formio.default_version`: `4.17.3`

## 16.0.10.6

Hide field `builder_id_domain` in `formio.form` form view.

## 16.0.10.5

### Form Builder UI improvements

- Sidebar panel disappears for long forms. This reverts some (resizing) changes from 16.0.7.0.
- Show the "Auto-save" setting in the dock before State.

## 16.0.10.4

Possibility to redirect the (parent) window upon submit of an embedded public form.

The redirect occurs if the `<iframe/>` has set:
- URL query-param `?embed` (any value allowed).
- Following `sandbox` attribute with values (AFAIK): `sandbox="allow-same-origin allow-scripts allow-top-navigation"`

### Example iframe

(Sizing weight/height is not covered here):

```html
<iframe src="https://www.example.com/formio/public/form/new/some-UUID?embed=1"
    sandbox="allow-same-origin allow-scripts allow-top-navigation"/>
```

## 16.0.10.3

Add Form component onBlur and onChange "Overlay timeout" (frontend) API.

## 16.0.10.2

Improvement for change in 16.0.8.3 (caching):\
Allow certain URLs (routes) to accept query (params) string.\
This ensures no WARNINGs `... called ignoring args ...` will appear in the Odoo server log.

## 16.0.10.1

Update system parameter `formio.default_version`: `4.17.2`

## 16.0.10.0

CSRF protection for forms. To protect the submit endpoints from abuse and spam.

This also removes the custom JSON-RPC implementation with XMLHttpRequest (XHR), which is still jQuery (to be replaced by native XHR soon).

Also removed several unused `kwargs` from controller methods (arguments).

## 16.0.9.2

Fix public form submit endpoint.\
Revert (accidentally) removed `import` in public controller.

## 16.0.9.1

Fix UI rendering of a public (existing) form.\
JS Console error: `Uncaught ReferenceError: importPath is not defined`

## 16.0.9.0

Fix sequence of form events and its async callback actions, by queue-ing the sequence of async callback actions into a Promise object.\
This ensures the sequence of async callback actions will be resolved (executed) in the same order of the JS event stack.

## 16.0.8.3

Form improvement:\
Avoid browser caching for Form assets files (CSS, JS).

## 16.0.8.2

Form Builder default Auto Save enabled.\
Because Odoo also does.

## 16.0.8.1

Improvement:\
Bypass any 'Administration/Access Rights' access error in the low-level method `_get_builder_from_id` used with form creation etc.\
Use `sudo` in `formio.form` method `_get_builder_from_id`.\
This is considered safe, because it's a low-level method.

## 16.0.8.0

### Improvements

Form UI overlay, to block user interaction while loading and upon wizard state and submission.

Advanced Form submit endpoint and response handling:\
In the client/browser (JS), upon form submission return the form its `submission_data` (JSON) in the response and write it to the (JS) formio.js form object.\
This allows to update the form (data) by backend/server code from the `submission_data` in the response.

Debug logging the `/submit` endpoints, by enabling the new "Debug Mode" field in the Form Builder.

Some Python code (Black) formatting improvements.

## 16.0.7.2

Form Builder improvement:\
Avoid browser caching for Form Builder assets files (CSS, JS).

## 16.0.7.1

Form Builder layout and styling improvements:
- Revert (accidental) removal of language buttons CSS.
- Improve spacing between language buttons and actions (save form button, auto-save message).

## 16.0.7.0

Form Builder improvements:
- Automatically resize the height.
- Auto-save or manual-save (switch) per Form Builder design.
- Remove the 'Fullscreen' mode (button), which causes resizer issue.
- Changes some from HTML (CSS) classes to ids.

## 16.0.6.11

Add current language (`res.lang`) IETF code/tag to the form `componentChange` payload.

## 16.0.6.10

Rename label of `formio.form` field `submission_data`, from `Data` to `Submission Data`.

## 16.0.6.9

Add `formio.form` (Form) `after_save_draft` method and execute it in the `/submit` endpoints (backend, portal, public).

## 16.0.6.8

### Fix

Still one Form loading regression (bug) in template `formio_form_public_embed`.\
Due to incomplete implementation of the new (loading) spinner implementation in v16.0.6.6.

## 16.0.6.7

### Fix

Form loading on portal and public/website.\
Due to incomplete implementation of the new (loading) spinner implementation in v16.0.6.6.

### Improvement
Put the form builder (loading) spinner in dedicated `<div/>` which hides when the form builder has been rendered.

## 16.0.6.6

### Improvements

- Menu renaming: 'Forms' to 'Form Submissions'
- Put the form (loading) spinner in dedicated `<div/>` which hides when the form has been rendered.

## 16.0.6.5

Security fix / meaurement:\
Deny update of `submission_data` (field) upon form update, if the form has state 'Completed' or 'Cancelled'.

## 16.0.6.4

Updated Dutch translations (nl.po file).

## 16.0.6.3

Improvement for translations:\
- Add translate function in `formio.builder` model
- Set language (IETF code) in payload of `customValidation` hook.

## 16.0.6.2

In Form Builder form-view, add group "main" in top of the notebook/page "formio_components_api".

## 16.0.6.1

Fix standalone form (`formio.form`) record create, shouldn't set the `res_id`.\
This also results in a visible button to open the linked resource.

## 16.0.6.0

Changes:\
- Implement the formio.js `customValidation` hook, which XHR posts to the API / validation endpoint.
- Some code reorder, cleanup and comments.

## 16.0.5.2

Fix regression due to `16.0.5.0` regarding formio.js version assets with `ir_attachment.location` default or set to `file`.\
The (storage) location of the font files was wrong. It should be in the CSS assets directory, for correct (relative) resolving.

## 16.0.5.1

Ensure record rule(s) modifications are not reverted, so `noupdate="1"`.

## 16.0.5.0

PR [\#243](https://github.com/novacode-nl/odoo-formio/pull/243), with additional improvements.

Improve storing and serving frontend assets determined by the configurable `ir_attachment.location`.\
This supports particular Odoo instances with other storage mechanisms - eg S3 buckets, Azure files.\
Additionally, this will work for a multi-node installation, with an instance other than the one that stores the files.

## 16.0.4.5

Add to Python eval context of `ir.actions.server` code:
- `_logger` - logger object
- `os.getenv` - get (os) environment variable function

## 16.0.4.4

Fix and improve 'datetime' component localization and translations:\
- Fix and improve `patchRequireLibrary` (JS function) to gradually determine the arguments.
- Fix and improve Form Builder `setLanguage` to localize datetime components.

## 16.0.4.3

Ensure external JavaScript libraries get loaded as expected by a common CDN.\
This introduces the `patchRequireLibrary` (JS function) which alters some library URLs the formio.js `CDN` class fetches.\
Currently the Flatpickr localizations URLs are altered.

## 16.0.4.2

### Improvement

Render a new portal form by the generic QWeb form template.\
This ensures to apply any extra form builder config/settings.

## 16.0.4.1

Backwards formio.js compatibility fix:\
Apply `patchCDN` if there's an instantiated `Formio.cdn` object.

## 16.0.4.0

Make formio.js CDN for hot-loaded dependencies configurable.

### Description

Make use of the formio.js CDN class to override the base URL for all 3rd party assets that are loaded on-the-fly by formio.js lib.\
This includes for example ACE, CKEditor, Flatpickr, Quill etc.

The Cloudflare CDN is set as the default value.\
They have a page about the GDPR: https://www.cloudflare.com/trust-hub/gdpr/

It's also possible to override the default value to a (paid) GDPR-aware CDN like KeyCDN.com or GlobalConnect.no and host the required files there,\
or simply point it to the base URL of their Odoo install and ship the files.\
This would require pinning the formio.js version, since different versions of the library need different dependencies.

## 16.0.3.2

### Fix

Fix migration for version 16.0.3.1 - upgrade error:\
`UniqueViolation: duplicate key value violates unique constraint "ir_config_parameter_key_uniq"`

### Improvements

Style (highlight) active language button.

The "Forms" Button in the Form Builder view.

Archive functionality for formio.js versions (also unarchive and search filter).

Wizard draft autosave mode.\
This allows complex components to serialize their data on the form before submitting it.

## 16.0.3.1

Improve app/module installation, by downloading and installing a default formio.js library version after install.\
Also log a warning in case an error (eg ConnectionError) occurs.

## 16.0.3.0

### 1. Refactored the Form its Form Builder (field) domain/filter.

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

### 2. Add new feature which allows Form Builders in "Draft" or "Obsolete" state to be choosen in a new Form in the backend.

The 2 setting fields are available in the Form Builder:
- Use Draft in Backend
- Use Obsolete in Backend

## 16.0.2.11

In the Form Builder, implement conditional warning (also extendable) in case there are integrated APIs.\
This warns the Form Builder user about components being removed or updated, which could lead the API regression/breakage.

## 16.0.2.10

- Fix language determination (cascade) for public Form load by UUID.
- Add cascade delete on `formio_version_id` in model `formio.version.translation`.

## 16.0.2.9

Backend Forms layout improvements:
- Form resizing according to the Form Builder (setting) field `iFrame Resizer bodyMargin`.\
  Concerns the fieldname: `iframe_resizer_body_margin`
- Improve the form view (sheet) height and styling.

## 16.0.2.8

Update iframe-resizer v4.3.6 (JS library).

## 16.0.2.7

Add form/builder heightCalculationMethod 'taggedElement' targets in portal and public templates.

## 16.0.2.6

Change form 'heightCalculationMethod' from 'lowestElement' to 'taggedElement'.\
This solves issues for components with dynamic height, eg the collapsible Edit Grid (type `editgrid`).

## 16.0.2.5

Change form 'heightCalculationMethod' from 'grow' to 'lowestElement'.\
Improvement to scale dynamically form height.

## 16.0.2.4

Remove `formio.version` Many2many `translations` field.
Refactoring done and migrated in 16.0.2.0.

## 16.0.2.3

Fix the `formio.form` function `_get_public_form_js_locales` (wrong argument), called in the config route/endpoint.

Enable a portal and/or public Form to _redirect (page) to URL_ upon a _Save Draft is Done_.\
This can be set in new fields in the Form Builder:
- Portal Save-Draft Done URL
- Public Save-Draft Done URL

Enhance the public Form access-check, by allowing _custom_ implementation(s) configured by a new selection field `public_access_rule_type`,
with current choice `time_interval`\
Other `public_access_rule_type` choices with a inheritted `public_access` (method) check implementation can be implemented by modules and apps\
Updating this module also executes a migration, which ensures existing form builders set the `public_access_rule_type` field value to `time_interval`.

## 16.0.2.2

Fix formio.js version (action/button) _Download and install_ error:\
`ValueError: max() arg is an empty sequence`.\
Initialize the translations sequence properly.

## 16.0.2.1

Improvements for Version Translations (model: `formio.version.translation`):
- Compute and store origin (base translation, user added).
- Compute and show whether a copied (origin) base translation has been updated.
- Add sequence field. So translations can be ordered to ease admnistration and the translation override implementation.

Fix `name_get` method (models: `formio.translation`, `formio.version.translation`)

## 16.0.2.0

Major improvements for translations:
- Specific Version Translations instead of linking (Many2many) to the available Base Translations.
- Translations (overrides) of formio.js source properties in the form builder.

Add `noupdate=1` for the xmlid `formio.version_dummy` data (record).\
This prevents recreation when the dummy version has been archived (is inactive).

## 16.0.1.12

Fix the component data URL check in the Form JS (rendering) code.

## 16.0.1.11

Improve loading "Extra Assets" (js, css), by targetting `before` or `after` the core assets.

## 16.0.1.10

Form Builder: Disallow create and edit for field "formio.js version".

## 16.0.1.9

Form Builder Lock/Unlock buttons with primary color.

## 16.0.1.8

Fix portal /my page.

## 16.0.1.7

Improve Form Builder "Actions API" tab (layout and info).

## 16.0.1.6

Migrate (v15) datetime component localization and translations:
- Set `extra_assets` in controllers template vars.
- Implement locales administration and passing to the (JS) frontend.
- Set default and update the datetime (flatpickr) locale by language chooser in a form.

## 16.0.1.5

Improvements for administration of "Extra Assets" (js, css) with link/relation to attachments.\
Affected models: `formio.extra.asset`, `ir.attachment`.

## 16.0.1.4

Implement "Forms Ref" field on several models regarding assets and attachments:\
`formio.version.asset`, `formio.extra.asset`, `ir.attachment`\
This facilitates purposes like export/import tools.

## 16.0.1.3

Minor layout (width) fix in Form Builder Translations tab.

## 16.0.1.2

Improve form builder wizard save as draft: previous page, page clicked.

## 16.0.1.1

Fix deprecation warning in (http) controller `send_fonts_file`, by using Werkzeug's implementation.

## 16.0.1.0

Initial release.
