# Changelog

## 15.0.3.3

Fix `formiodata.Builder` language determination by IETF-code instead of ISO.

## 15.0.3.2

Remove previous (3.1) convert feature regarding Components API `formio.component.server.api`\
It was a bad idea. Can be done directly per component, but more verbose, in the Components value API.

## 15.0.3.1

Components API `formio.component.server.api`
- value conversion (convert) feature, which is a new API type.
- Unique constraint on fields `name`, `type`.

## 15.0.3.0

- Components API `formio.component.server.api`: change field `active` default value to `True` (checked).
- Implement ETL data/values for Form Builder (new form) by Components Server API.
- Renaming (improvement) argument in function `_get_formio_eval_context`, a feature added in version 2.2\
  Renaming from `data` to `params`.

**UPGRADE REQUIREMENT (important):**\
Check and rename `data` to `params` in existing `formio.component.server.api` records, in the Python `code` (field).\
Otherwise existing forms (builder) configurations with Componenets API (values, domain) won't work anymore!

## 15.0.2.2

Enable a new (not yet stored) form, to use the Components API as well.

It was necessary to refactor the method `_get_formio_eval_context`.\
This method is used by the Components API to apply on a `formio.builder` object and possibly obtain the `formio.form` object too.\
There's always a `formio.builder` object present, so it's the logical class to implement the method in anyway.\
The method accepts an optional `formio.form` object in the arguments.

## 15.0.2.1

Form builder: obtain (un)locked setting to allow editable *Components API* configuration.

## 15.0.2.0

(The following) changes to support advanced features for the components API.
- Add selection field `type` in model `formio.component.server.api`, with one value (`value`), which still represents the component server value API.
- Improve the function `_get_formio_eval_context`.

## 15.0.1.8

Upon Copy of Form Builder, copy the Component Server APIs as well.

## 15.0.1.7

Several fixes, especially in ETL of odoo data.

## 15.0.1.6

Fix `_etl_res_field_value` function: incorrect use of safe_eval causes exception.\
GitHub issue https://github.com/novacode-nl/odoo-formio/issues/173

## 15.0.1.5

Fix ETL (component value) `user_field`, which didn't traversed relational fields (eg Many2one object).\
GitHub issue https://github.com/novacode-nl/odoo-formio/issues/169

## 15.0.1.4

Fix `formio.form` language determination in `__getattr__` which gets the (Python) `formiodata` `Form` object.

## 15.0.1.3

Renaming (v1.2) ETL API implementation and usage (prefixes):
- FROM: `server_value_api`
- TO: `server_api`\
(!!) This is backwards incompatible and requires to change existing Form Builders which apply this feature since v1.2.

## 15.0.1.2

New ETL API feature: Get and set Component Value by Server (Python) Code.

## 15.0.1.1

Add global `noupdate_form` rule in component ETL API.\
This replaces `res_field_noupdate_form`, introduced in version 1.0.

## 15.0.1.0

MAJOR IMPROVEMENT of the component ETL API, to load and prefill data from Odoo field(s).\
 This is a major change that greatly improves ease of use, flexibility and new features to come.\
The previous API/usage (in Property Name, aka the component key) is still supported, but deprecated and logs a DEPRECATION warning.

## 15.0.0.9

Pass determined (lang) `date_format` and `time_format` to the `Form` object contructor.

## 15.0.0.8

- New ETL API: `OdooUser`\
ETL a field from *current user* (logged-in uswr) into the Form.
- Change ETL API: `Odoo`\
This now ETL a field from the Resource model object into the Form, also when Form has *state = DRAFT*
- Change ETL API: `OdooModel`\
ETL a field from the linked *Resource model object* into the Form.\
(!!) This is backwards incompatible and requires to change existing Form Builders to: `OdooModel__model`

## 15.0.0.7

Fix/change due to recent change in the Python `formiodata` library (version: 0.3.0)\
Change (formiodata) `Builder` object attr: `form_components` became `input_components`

## 15.0.0.6

New API feature, support for Mail Template:\
Form model object (`formio.form`) can now be used in a Mail Template (Jinja template renderer), e.g. to show field value, select choices etc.\
This extends the *Mail Render Mixin*, because the *Jinja Sandbox* object doesn't directly allow `${object._formio}`, which it treats as unsafe and throws an exception.

USAGE EXAMPLE (where `object` is a `formio.form` model object):\
`${formio(object).input.firstName.value}`

## 15.0.0.5

Remove silly model determination by `initial_res_model_id`.\
The current model is always stored and present in `res_model_id`.

## 15.0.0.4

New API feature `OdooModel`\
ETL the Odoo model name into Forms (API Property Name: `OdooModel`).

## 15.0.0.3

Change ETL Odoo field-data (API): field delimter from "`.`" to "`__`" (2 underscores).
- A dot "`.`" results in undesired submission data, due to the formio Javascript library/API.
- A dash "`/`" is allowed, however causing issues with the ETL module (formio_etl).

## 15.0.0.2

New API features `Odoo` and `OdooRF`

## 15.0.0.1

Initial version
