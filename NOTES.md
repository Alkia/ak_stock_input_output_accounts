# Design notes

## Stock Account vs Stock Valuation Account

**Yes — they are the same thing.** The field `property_stock_valuation_account_id` on product category is the balance-sheet account where the value of stock is held. In the UI we label it **"Stock Account"**; other Odoo screens may call it "Stock Valuation Account". Same field, same meaning.

---

## Price Difference Account

**It is in the module.** The field `property_ak_stock_price_difference_categ_id` (label: **Price Difference Account**) is:

- Defined in `models/product_category.py`.
- Shown in the **Account Properties** section of the Product Category form when **Inventory Valuation** is *Periodic (at closing)* (`invisible` when `property_valuation != 'manual_periodic'`).

It was temporarily removed from the view only to get the module to install on environments where the addon’s Python was not yet loaded (view validation failed with “field does not exist”). It is now back in the view. If you still see “field does not exist” on install, ensure the full addon (including `models/product_category.py`) is deployed and Odoo is restarted before installing/upgrading.

---

## Stock Variation

**Removed because Odoo 19 no longer has it on product.category.** The standard field `property_stock_variation_account_id` was dropped from the `product.category` model in Odoo 19. Our view inherited the stock_account form that originally showed it; at install we got:

`Field "property_stock_variation_account_id" does not exist in model "product.category"`

So we removed it from the view. To have a “Stock Variation” account again you would need to:

1. Add a new field on `product.category` in this module (e.g. `property_ak_stock_variation_account_id`).
2. Add it to the Product Category form view.
3. Use it in your own logic (e.g. stock revaluation) if required.

---

## Stock Journal (where stock moves are posted)

In Odoo, inventory valuation entries are posted to a **journal** (e.g. “Stock Valuation” or “Inventory”). That journal is usually set at **company / inventory settings** level, not per product category. So:

- **Default behaviour:** One stock journal per company (or per warehouse) is configured in Settings; all stock valuation moves for that company/warehouse use that journal. No “Stock Journal” field on product category is required for standard behaviour.
- **If you want a Stock Journal on the category:** You can add a Many2one to `account.journal` on `product.category` (e.g. `property_stock_journal_categ_id`) and use it when posting moves for products in that category. That gives per-category control but is not the standard Odoo setup.

This module does **not** add a Stock Journal field on product category. If you want it, we can add `property_ak_stock_journal_categ_id` (or similar) and a place in the form view.
