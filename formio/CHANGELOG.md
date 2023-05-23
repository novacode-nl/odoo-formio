# Changelog

## 16.0.2.2

Fix formio.js version (action/button) _Download and install_ error:\
`ValueError: max() arg is an empty sequence`.\
Initialize the translations sequence properly.

When there's no

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

Add `noupdate=1` for the xmlid `formio.version_dummy` data (record).
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

Fix deprecation warning in (http) controller `send_fonts_file`, by
using Werkzeug's implementation.

## 16.0.1.0

Initial release.
