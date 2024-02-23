# Odoo CRM Leads with Formio Forms Integration

This module extends the functionality of Odoo CRM Leads by integrating Formio forms, allowing users to associate dynamic forms with CRM leads. It adds a seamless way to create, manage, and track custom forms directly from the CRM leads interface.

## Features

- Link multiple Formio forms to a single CRM lead.
- Automatically update forms linked to a CRM lead when the lead's information changes.
- View and manage all forms associated with a CRM lead directly from the CRM lead's form view.
- A counter on the CRM lead form shows the number of linked Formio forms.
- Direct navigation to related Formio forms with full support for Kanban, Tree, and Form views.

## Installation

To install this module, you need to:

1. Clone the repository into your Odoo addons directory:
   ```
   cd /path/to/your/addons
   git clone git@github.com:novacode-nl/odoo-formio.git --branch 15.0
   ```
2. Update the Odoo addons list by navigating to the Apps menu and clicking on the "Update Apps List" link.
3. Install the module by searching for "CRM Leads with Formio Forms Integration" in the Apps menu and clicking the Install button.

## Configuration

No additional configuration is required beyond installing the module. It automatically adds the necessary fields and actions to the CRM Lead model.

## Usage

After installation, follow these steps to use the integration:

1. Open any CRM lead in the Odoo backend.
2. Navigate to the "Forms" tab or section where you will see the linked Formio forms.
3. To link a new Formio form to the lead, click on the action button to create or link an existing form. The module will automatically relate the form to the current lead.
4. Use the "Forms Count" on the CRM lead form to quickly see the number of linked forms.

## Development

This module introduces two main extensions:

- **CrmLead**: This model is extended to include fields for linking Formio forms and managing the count and actions related to these forms.
- **Form**: The Formio form model is extended to include a reference to the CRM lead it's associated with and to ensure that form updates reflect on the related CRM lead.

### Overridden Methods

- `write` on `CrmLead`: Ensures that any updates to the CRM lead's name are propagated to the linked Formio forms.
- `_prepare_create_vals` on `Form`: Prepares the creation values for a new Formio form linked to a CRM lead, including setting the lead's partner as the form's partner.

## License

This module is published under the GPL license, as mentioned in the LICENSE file included in this repository. Please see the LICENSE file in the repository for the full text.

For more information and assistance, please contact [Nova Code](http://www.novacode.nl).

---

Note: Replace `[LICENSE]` with the actual license type (e.g., LGPL, AGPL) used by Nova Code for this module, and adjust the repository URL and contact details as necessary.
