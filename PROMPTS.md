# Prompts

This file records prompts used to evolve the **AK Stock Input/Output Accounts** module.

---

## Product Categories: add Price Difference, Stock Input, Stock Output

**Prompt (cleaned up):**

The Odoo Product Categories form already shows all fields from the reference screenshot (Logistics, Account Properties, Inventory Valuation). Add the following three fields and ensure they install without problems:

1. **Price Difference Account**
   - **Field:** `property_account_creditor_price_difference_categ_id`
   - **Model:** `product.category`
   - **Type:** Many2one → `account.account`
   - **Context:** `{}`
   - **Domain:** `[('deprecated', '=', False)]`
   - **Modifiers:** Invisible when `property_valuation != 'manual_periodic'`
   - **Placement:** In the **Account Properties** section.

2. **Stock Input Account**
   - **Field:** `property_stock_account_input_categ_id`
   - **Model:** `product.category`
   - **Type:** Many2one → `account.account`
   - **Context:** `{}`
   - **Domain:** `['|', ('company_id', '=', False), ('company_id', 'in', allowed_company_ids)]`
   - **Modifiers:** Required when `property_valuation == 'real_time'`
   - **Description:** Counterpart journal items for all incoming stock moves will be posted in this account, unless there is a specific valuation account set on the source location. This is the default value for all products in this category. It can also directly be set on each product.
   - **Placement:** In the **Account Stock Properties** section.

3. **Stock Output Account**
   - **Field:** `property_stock_account_output_categ_id`
   - **Model:** `product.category`
   - **Type:** Many2one → `account.account`
   - **Context:** `{}`
   - **Domain:** `['|', ('company_id', '=', False), ('company_id', 'in', allowed_company_ids), ('deprecated', '=', False)]`
   - **Modifiers:** Required when `property_valuation == 'real_time'`
   - **Description:** When doing automated inventory valuation, counterpart journal items for all outgoing stock moves will be posted in this account, unless there is a specific valuation account set on the destination location. This is the default value for all products in this category. It can also directly be set on each product.
   - **Placement:** In the **Account Stock Properties** section.

Check the project structure and manifest so the module installs without problems.

---

## Security (ir.model.access)

**Is `security/ir.model.access.csv` OK?**

Yes. This module does **not** define any new models (`_name`). It only **inherits** existing models:

- `product.category` (from `product` / `stock_account`)
- `purchase.order` (from `purchase`)

Access rights are defined on the base models. Inherited models use the same `ir.model.access` rules as the base, so no extra lines are needed in `ir.model.access.csv`. The file only contains the header and no data rows, which is correct for a module that adds no new models.

If you add a new model (e.g. `_name = 'ak.stock.something'`) later, you must add a corresponding line in `ir.model.access.csv` and reference the file in `__manifest__.py` under `'data'`.

---

## Fields visible on Product Categories (detailed)

Below is a detailed list of fields that appear on the **Product Categories** form when this module is installed. The form is built from the base **stock_account** view plus this module’s inheritance.

### Section: **Account Properties**  
*(group: `account_properties`, group restriction: `account.group_account_readonly`)*

| Label (UI) | Field name | Type | Description / behavior |
|------------|------------|------|-------------------------|
| **Stock Account** | `property_stock_valuation_account_id` | Many2one → account.account | Main stock valuation account for the category. |
| **Stock Variation** | `property_stock_variation_account_id` | Many2one → account.account | Account for stock value variations (e.g. revaluation). |
| **Income Account** | `property_account_income_categ_id` | Many2one → account.account | Default income account for products in this category. |
| **Expense Account** | `property_account_expense_categ_id` | Many2one → account.account | Default expense account for products in this category. |
| **Price variance (PO vs Bill)** | `property_stock_account_price_difference_categ_id` | Many2one → account.account | Account for purchase price variance (PO vs bill). Domain limits to certain account types and company. |
| **Price Difference Account** | `property_account_creditor_price_difference_categ_id` | Many2one → account.account | Account for price differences (e.g. creditor/valuation). **Visible only when** Inventory Valuation = *Periodic (manual_periodic)*. Domain: non-deprecated accounts. |

### Section: **Account Stock Properties**  
*(group: `account_stock_properties`, group restriction: `account.group_account_readonly`)*

| Label (UI) | Field name | Type | Description / behavior |
|------------|------------|------|-------------------------|
| **Stock Account** | `property_stock_valuation_account_id` | Many2one → account.account | Same valuation account as above, shown again in this block. |
| **Stock Input Account** | `property_stock_account_input_categ_id` | Many2one → account.account | Default account for **incoming** stock moves (e.g. GRNI / stock interim received). Counterpart journal items for all incoming moves use this unless the source location has a specific valuation account. **Required when** Inventory Valuation = *Perpetual (real_time)*. Domain: current company or no company. |
| **Stock Output Account** | `property_stock_account_output_categ_id` | Many2one → account.account | Default account for **outgoing** stock moves (e.g. stock interim delivered). Counterpart journal items for all outgoing moves use this unless the destination location has a specific valuation account. **Required when** Inventory Valuation = *Perpetual (real_time)*. Domain: current company or no company, non-deprecated. |

### Section: **Logistics**  
*(from base product / stock views)*

| Label (UI) | Field name | Type | Description / behavior |
|------------|------------|------|-------------------------|
| **Force Removal Strategy?** | (from base) | – | Removal strategy override for the category. |

### Section: **Inventory Valuation**  
*(from base stock_account view)*

| Label (UI) | Field name | Type | Description / behavior |
|------------|------------|------|-------------------------|
| **Costing Method** | (e.g. costing_method) | Selection | Standard price, FIFO, etc. |
| **Inventory Valuation** | `property_valuation` | Selection | *Periodic (at closing)* (`manual_periodic`) or *Perpetual (real time)* (`real_time`). Drives visibility of **Price Difference Account** and required state of **Stock Input** / **Stock Output**. |

---

### Summary of module-specific fields

- **Price Difference Account** — `property_account_creditor_price_difference_categ_id` (visible only for *Periodic* valuation).
- **Stock Input Account** — `property_stock_account_input_categ_id` (required for *Perpetual* valuation).
- **Stock Output Account** — `property_stock_account_output_categ_id` (required for *Perpetual* valuation).

All three are company-dependent Many2one fields to `account.account` and appear on the Product Categories form as in the table above.
