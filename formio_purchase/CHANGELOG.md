# Changelog

## 2.0

Replace the `_onchange_builder_id` method (implementation) by a new method `_get_builder_domain`.\
This due to refactoring in the base Forms (`formio`) module, to solve a deprecation warning,
regarding a domain that may not be returned by an onchange method.

## 1.0

Initial release.
