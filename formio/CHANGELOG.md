# Changelog

## 16.0.1.6

Migrate (v15) datetime component localization and translations:
- Set `extra_assets` in controllers template vars.
- Implement locales administration and passing to the (JS) frontend.
- Set default and update the datetime (flatpickr) locale by language chooser in a form.

## 16.0.1.5

Improvements for administration of "Extra Assets" (js, css) with link/relation to attachments.\
Affected models: `formio.extra.attachment`, `ir.attachment`.

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
