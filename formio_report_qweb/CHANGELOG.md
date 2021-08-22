# Changelog

## 3.3

- New component: `survey`

## 3.2

- Improve `password` component: show no mask (only empty input field) if value is empty.

## 3.1

- Fix and improve `day` component to obtain format (position) of Month and Day.

## 3.0

- MAJOR IMPROVEMENT: "Simple" conditional visibility of components, by checking new property `component.is_visible`\
  Possible by recent improvements in the Python formiodata library (version: 0.3.3).\

This release is backwards incompatible for overrides/customizations of the following QWeb XML.\
Moved the visibility check:\
- From: `<template id="report_formio_form_template> ... <t t-if="component.hidden != True>`
- To: `<template id="component"> ... <t t-if="component.is_visible">`

## 2.1

- New input component: `day`
- New component: `htmlelement`
- Fix report "Form (My preferences)", to render in the current user language. (QWeb report: `report_formio_form_document`)

## 2.0

- MAJOR IMPROVEMENT: Rendering of nested components e.g. in `datagrid`, `layout` components.\
  Possible by recent improvements in the Python `formiodata` library (version: 0.3.0).
- Don't escape a component label (let's trust this). This ensures the label (inner) HTML/styling shall be preserved in reports.

This release is backwards incompatible (eg in case of implemented custom QWeb Reports which inherit from this QWeb XML).

## 1.1

- Fix and re-implement components (file, content/html, table, tabs), which got broken after recent changes in 2.0.

## 1.0

- New input component: `datetime`
- Improve rendering of nested components e.g. in `datagrid`, `layout` components.\
  Possible by recent improvements in the Python formiodata library (version: 0.2.0).
- Improve rendering of `datagrid` component.
  Possible by recent improvements in the Python formiodata library (version: 0.2.0).
- Improve `columns` component:
  - Complex columns/grids with identical layout (row wrapping ) as in the Form. For example 3 rows with specified column widths `[[6,6], [12], [8, 4]]`.
  - The QWeb component (object) is now the Python `formiodata Component` object, instead of a Dictionary `component['_object']`.
  
This release is backwards incompatible, in case of implemented custom QWeb Reports which inherit from this QWeb XML.

## 0.12

- New input component: `radio`

## 0.11

- New input component: `datagrid`
- Refactor component (object) loading/reader.

## 0.10

- New input component: `file`\
  (Eg used for upload. Storage provider: base64)

## 0.9

- Don't render `hidden` components.
- Smaller report header (h3 instead of h2).

## 0.8

- Don't render the `file` component if not an image.

## 0.7

- New layout components:
  - `table`
  - `tabs`

## 0.6

- New input components:
  - `email`
  - `content`
  - `number`
  - `phoneNumber`
  - `signature` (image)

## 0.5

- Annotate required components
- Render not stored (optional and empty) components.

## 0.4

- Reports configuration per Builder:\
  Show not implemented components/fields (setting and implementation).\
  Improves the feature introduced in version 0.3.
    
## 0.3

- Render not implemented components (raw data) with a warning.
    
## 0.2

- New input component: `select` (one, multiple)
- Some layout/design improvements.

## 0.1

- Initial version with components:
  - `textfield`
  - `textarea`
  - `number`
  - `selectboxes`
  - `checkbox`
  - `columns` (layout)
  - `panel` (layout)
