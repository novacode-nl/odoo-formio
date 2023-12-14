# Changelog

## 16.0.1.3

Move the `formio.form` `markupsafe()` instance method to the `formio_data_api` module.\
That's the logical place, because it's needed in other modules and parts (eg email templates).

## 16.0.1.2

Use MarkupSafe to escape components:
- content_component
- html_component
- textarea_component

## 16.0.1.1

Layout improvements for the report components, to comply with the (Odoo) Bootstrap upgrade from v4 to v5.

## 16.0.1.0

Initial release.
