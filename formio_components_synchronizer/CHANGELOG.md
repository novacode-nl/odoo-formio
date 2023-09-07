# Changelog

## 16.0.2.1

Add Component properties (model fields and views):
- `hidden`: Display // Hidden
- `disabled`: Display // Disabled
- `tableView`: Display // Table View
- `disabled`: Display // Disabled
- `clear_on_hide`: Data // Clear Value When Hidden
- `required`: Validation // Required
- `validate`: Validation (validations: simple, custom and JSON)
- `properties`: API // Custom Properties
- `conditional`: Conditional // Simple Conditional
- `custom_conditional`: Conditional // Custom Conditional
- `templates`: Templates (eg templates for layout and (data) grids.)
- `logic`: Logic (trigger/action pairs).

Improve the update component implementation, by checking changed/updated components against fields.

Some views improvements.

## 16.0.2.0

- Fix module v16.0 migration.
- Add fields to the Component record, to show the (full, input) paths with keys and labels in the related Form Builder.
- Distinguish input and layout components. Therefor add `formio.component` boolean field `input`.
- Other improvements.

## 16.0.1.0

Initial release.
