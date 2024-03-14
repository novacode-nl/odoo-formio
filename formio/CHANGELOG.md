# Changelog

## 17.0.1.3

Add new group "Forms: Allow updating form submission data".\
Users in this group are allowed to edit and update the (raw, JSON) submission data in the `formio.form` form view.

## 17.0.1.2

- Fix formioScrollIntoView event handler.
- Default value for form builder fields: `portal_scroll_into_view`, `public_scroll_into_view`

## 17.0.1.1

Improve the formio.js library registration (downloader, importer) with a new setting to allow only registered versions.\
This adds a new system parameter `ir.config_parameter` which currently defaults to 'v4' and can be modified in the configuration window.\
The allowed setting is a comma separated string (list) of formio.js versions to register. Examples:
- v4,v5
- v4.17,v4.18

## 17.0.1.0

Initial release.
