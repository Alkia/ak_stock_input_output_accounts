# Installation

## Deploy the full addon

Odoo loads **Python first**, then **XML**. Both must be from this module.

- Copy the **entire** folder `ak_stock_input_output_accounts` to your Odoo addons path (e.g. `/mnt/extra-addons/`).
- Ensure these files are updated on the server:
  - `models/product_category.py` (defines `property_ak_stock_price_difference_categ_id`, etc.)
  - `views/product_category_views.xml`
- **Restart the Odoo process** so Python modules are reloaded (not only the browser).
- Then in Odoo: **Apps** → find **Restore Stock Input/Output Accounts in v19** → **Install** or **Upgrade**.

## If you see "Field ... does not exist in model product.category"

The server is using **new XML** but **old Python**. Fix:

1. Copy `addons/ak_stock_input_output_accounts/models/product_category.py` to the server (same path under the addon).
2. Restart Odoo (full process restart).
3. Install or upgrade the module again.

## If you see "Unknown field account.account.deprecated in domain"

You are using an old view or an old Python field that still uses a `deprecated` domain. Use the current addon version (Price Difference field name: `property_ak_stock_price_difference_categ_id`, no domain on account fields).

## If you see "column product_category.property_ak_stock_variation_account_id does not exist"

The **Python** model defines this field but the **database** never got the column (e.g. module was not upgraded after the field was added). This can happen when validating a stock picking because Odoo touches product categories.

**Fix:** Run a proper module upgrade so Odoo adds the missing column:

1. Deploy the full addon (including `models/product_category.py`).
2. **Restart Odoo** (full process restart).
3. **Upgrade** the module: **Apps** → find **Restore Stock Input/Output Accounts in v19** → **Upgrade** (or from shell: `odoo-bin -u ak_stock_input_output_accounts -d your_db`).

After the upgrade, the table `product_category` will have the new column and the error will stop. This is **not** related to the Inventory Valuation journal (STJ) or to posting; it is a schema sync issue.
