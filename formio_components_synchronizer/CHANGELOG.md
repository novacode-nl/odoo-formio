# Changelog

## 15.0.1.1

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

## 15.0.1.0
- Add fields to the Component record, to show the (full, input) paths with keys and labels in the related Form Builder.
- Distinguish input and layout components. Therefor add `formio.component` boolean field `input`.
- Other improvements.

## 15.0.0.2

- Fix `name_get` method.
- Add One2many `component_ids` on `formio.builder`.

## 15.0.0.1

- Initial version.
