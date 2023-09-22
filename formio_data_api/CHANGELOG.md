# Changelog

## 16.0.2.0

Ability to set the `formiodata.Builder` instantiation its `component_class_mapping` property.\
This can be provided as a Dictionary on the `formio.form` its `context`, by the keyword argument `formio_component_class_mapping`.

Example:

```python
component_class_mapping = {'nova_editgrid': 'editgrid'}

form = (
    self.env["formio.form"]
    .with_context(formio_component_class_mapping=component_class_mapping)
    .get_form(uuid, 'read')
)
```

More info: https://github.com/novacode-nl/python-formio-data \
Checkout the README and unittest (file): `tests/test_component_class_mapping.py`

## 16.0.1.1

Fix `formiodata.Builder` language determination by IETF-code instead of ISO.

## 16.0.1.0

Initial release.
