# Changelog

## 2.0

Replace the `_onchange_builder_id` method (implementation) by a new method `_get_builder_domain`.\
This due to refactoring in the base Forms (`formio`) module, to solve a deprecation warning,
regarding a domain that may not be returned by an onchange method.

## 1.2

- Fix `write` function in partner model.\
Which could update the form's `res_name` field, when the partner name has been updated.\
Even when the user doesn't has forms access, the (write) function is allowed to update the field in forms.

## 1.1

- Fix computed fields: access rights (compute_sudo).
- Fix Forms button in partner/contact form: access right.

## 1.0

- Remove field `base_res_partner_id`. From now on use `partner_id` present in the formio (base) module.
- Data migration which updates/stores `formio_form.base_res_partner_id` into `formio_form.partner_id`.

## 0.2

Minor changes.

## 0.1

Initial draft release.
