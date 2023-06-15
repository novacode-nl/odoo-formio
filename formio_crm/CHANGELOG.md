# Changelog

## 16.0.2.0

Replace the `_onchange_builder_id` method (implementation) by a new method `_get_builder_domain`.\
This due to refactoring in the base Forms (`formio`) module, to solve a deprecation warning,
regarding a domain that may not be returned by an onchange method.

## 16.0.1.1

Add cascade delete on `crm_lead_id` field in `formio.form` model.

## 16.0.1.0

Initial release.
