# Create in the Product Category a Third option: "Perpetual++ (at reception and invoicing)"

This document outlines **step by step** what is required to add a third inventory valuation option **"Perpetual (at reception and invoicing)"** where accounting entries are created:

1. **At reception** – when a product is received (stock move done).
2. **At billing** – when a vendor bill is validated.
3. **At invoicing** – when a customer invoice is validated.

---

## Current Odoo behaviour (reference)

- **Periodic (at closing)** (`manual_periodic`): No automatic entries at receipt/delivery; valuation and entries at period end.
- **Perpetual (real time)** (`real_time`): Entries at receipt and delivery (Stock Input / Stock Output), using the Inventory Valuation journal.

The new option should behave like a hybrid: **entry at reception** (e.g. Stock Input / GRNI), then **entry at vendor bill** (clear GRNI, post expense), and **entry at customer invoice** (revenue, COGS).

---

## Step-by-step implementation plan

### Step 1: Add the new valuation value to the selection field

- **Where:** The field that drives valuation is usually `property_valuation` on `product.category` (or `product.template`), defined in **stock_account** or stock.
- **Action:**
  - Locate the selection definition (e.g. `_get_property_valuation` or a `Selection` field with `manual_periodic` and `real_time`).
  - Add a third value, e.g. `perpetual_reception_invoicing` (or `anglo_saxon` if you want to align with that naming).
- **In our module:** Extend `product.category` (or the model that holds the field) and **override** the selection to add the new choice. If the field is defined on `product.template`, extend that instead.
- **UI label:** `"Perpetual++ (at reception and invoicing)"`.

**Deliverable:** Product categories can be set to the new valuation method.

---

### Step 2: Expose the new option in the Product Category form

- **Where:** The Inventory Valuation field is shown in the category form (base view from stock_account).
- **Action:**
  - If the selection is extended in Step 1, the new value appears automatically in the dropdown.
  - Otherwise, inherit the view that contains the Inventory Valuation field and ensure the options include the new value (or the field is not restricted to only two choices).
- **Optional:** In our product category view, set `required="property_valuation == 'real_time'"` only for real_time; for the new option you may want Stock Input/Output **optional** or **required** depending on design (see Step 3).

**Deliverable:** User can select "Perpetual (at reception and invoicing)" in the category form.

---

### Step 3: Define when to create entries (reception vs bill vs invoice)

- **At reception:** Create a journal entry (e.g. DR Stock Input / GRNI, CR Stock Valuation or equivalent) when the **stock move** is set to done. Use the **Inventory Valuation** journal (e.g. STJ) and the category’s **Stock Input Account** (and Stock Account if applicable).
- **At vendor bill:** When a **vendor bill** (`account.move` type `in_invoice`) is posted, create/update entries: e.g. DR Expense, CR Stock Input / GRNI (clear interim), and handle price difference if any (Price Difference Account). Use the bill’s journal.
- **At customer invoice:** When a **customer invoice** (`account.move` type `out_invoice`) is posted, create entries for revenue and COGS (e.g. DR COGS, CR Stock Output; DR Receivable, CR Revenue). Use the invoice journal.

So you need three hooks: **stock move done**, **vendor bill post**, **customer invoice post**.

---

### Step 4: Hook into stock move completion (reception)

- **Where:** In **stock_account**, stock moves create valuation layers and often journal entries in methods such as:
  - `stock.move` → `_action_done()` or `_run_valuation()` / `_create_valuation_layer()` and the method that posts the **account move** (e.g. `_account_entry_move()` or similar).
- **Action:**
  - In our module, **inherit** `stock.move` (from stock_account) and override the method that decides whether to create an accounting entry and which accounts to use.
  - If the move’s product (category) has `property_valuation == 'perpetual_reception_invoicing'` (your new value), then:
    - Create the **stock valuation layer** (if applicable).
    - Create the **account.move** (journal entry) using:
      - **Journal:** The company’s **Inventory Valuation** journal (STJ).
      - **Accounts:** Category’s **Stock Input Account** (for in) or **Stock Output Account** (for out), and **Stock Account** (valuation), following the same logic as `real_time` but ensuring it runs for your new option.
  - Reuse or mirror the logic used for `real_time` so that reception posts one entry; only the condition on `property_valuation` changes to include your new value.

**Deliverable:** Receiving a product (picking validate) creates an automatic accounting entry in the Inventory Valuation journal (STJ) for categories using "Perpetual (at reception and invoicing)".

---

### Step 5: Hook into vendor bill posting (billing)

- **Where:** **purchase** / **stock_account**: when a vendor bill is validated, it often reconciles with purchase order and stock (e.g. `account.move` with `purchase_line_id` or link to stock moves / SVL).
- **Action:**
  - Find where vendor bills (`account.move`, `move_type == 'in_invoice'`) are posted and where **stock valuation** or **expense** entries are created (e.g. in `account.move` or in a method called on bill validation).
  - Extend that flow so that when the bill concerns products whose category uses `perpetual_reception_invoicing`:
    - Create or complete the entry that:
      - Clears the **Stock Input / GRNI** (or equivalent interim account) and
      - Posts to **Expense** (and **Price Difference Account** if unit price on bill differs from receipt).
  - Use the **bill’s journal** for this move (or the same journal as the rest of the bill).
  - Ensure you use the category’s **Stock Input Account**, **Expense Account**, and **Price Difference Account** where relevant.

**Deliverable:** Posting a vendor bill creates/updates the accounting entry so that the reception entry is closed and expense (and price difference) is recorded.

---

### Step 6: Hook into customer invoice posting (invoicing)

- **Where:** **sale** / **stock_account**: when a customer invoice is validated, revenue and sometimes COGS are posted.
- **Action:**
  - Find where **customer invoices** (`account.move`, `move_type == 'out_invoice'`) are posted and where **revenue** and **COGS** lines are created.
  - For categories with `perpetual_reception_invoicing`:
    - Ensure the **revenue** entry (e.g. CR Income) is created when the invoice is posted.
    - Ensure the **COGS** entry is created at invoice (e.g. DR Expense/COGS, CR Stock Output or Stock Account), using the category’s **Stock Output Account** and **Expense Account**.
  - Use the **invoice’s journal** for these lines.

**Deliverable:** Posting a customer invoice creates the revenue and COGS entries for products in categories using this method.

---

### Step 7: Journals and accounts

- **Reception:** Use the **Inventory Valuation** journal (e.g. STJ) – same as for "Perpetual (real time)". Ensure the category has **Stock Input Account** and **Stock Account** (and **Stock Output Account** for outbound moves) set.
- **Vendor bill:** Use the **bill’s journal**; accounts from category: Expense, Stock Input (to clear), Price Difference if needed.
- **Customer invoice:** Use the **invoice’s journal**; accounts from category: Income, Expense/COGS, Stock Output (to clear).

No need for a separate “reception and invoicing” journal: reuse STJ for stock moves and the bill/invoice journals for the rest.

---

### Step 8: Testing and edge cases

- **Receive then bill (purchase):** Receive 10, bill 10 → reception entry first, then bill entry clears GRNI and posts expense.
- **Receive 10, bill 8:** Define policy for partial billing (e.g. clear GRNI proportionally or only when fully billed).
- **Delivery then invoice (sale):** Deliver 10, invoice 10 → delivery entry (if you post at delivery for this option) or only at invoice; then invoice posts revenue + COGS. (Clarify whether “at reception and invoicing” means you also post at delivery or only at customer invoice.)
- **Price difference:** Bill price ≠ receipt price → use **Price Difference Account** in the bill’s journal entry.

---

### Step 9: Dependencies and manifest

- **Depends:** This module already depends on `stock_account` and `purchase`. If you need to extend **sale** or **sale_stock** for the customer-invoice part, add `sale` (or `sale_stock`) to `depends` in `__manifest__.py`.
- **Data:** No extra view is strictly required for the selection if you extend the field in Python; only ensure the form shows the Inventory Valuation field (already there).

---

### Step 10: Documentation and user guidance

- In **Product Category** form or in Help, document that "Perpetual (at reception and invoicing)" means:
  - An accounting entry is created **when the product is received** (Stock Input / GRNI in STJ).
  - Entries are created/updated **when the product is billed** (vendor bill journal).
  - Entries are created **when the product is invoiced** (customer invoice journal).
- Optionally add a short note in **README.md** or **NOTES.md** describing the third option and which accounts/journals are used.

---

## Summary checklist

| Step | What | Where / How |
|------|------|-------------|
| 1 | Add selection value `perpetual_reception_invoicing` | Extend `property_valuation` on product.category (or product.template) |
| 2 | Show new option in UI | Same field; ensure view shows it |
| 3 | Define rules (reception / bill / invoice) | Design doc or spec |
| 4 | Reception → create entry | Extend stock.move (stock_account), post move in STJ with Stock Input/Output |
| 5 | Vendor bill → create/update entry | Extend account.move or purchase/stock_account bill logic; clear GRNI, post expense |
| 6 | Customer invoice → create entry | Extend account.move or sale logic; post revenue + COGS |
| 7 | Journals | STJ for reception; bill/invoice journals for the rest |
| 8 | Tests | Partial bill, price difference, delivery then invoice |
| 9 | Manifest | Add sale/sale_stock if needed |
| 10 | Docs | Explain the third option and when entries are posted |

---

## Note

The exact method names and file locations depend on your **Odoo 19** codebase (community/enterprise). Use your project’s `stock_account` and `purchase` (and `sale`) addons to find the current methods that create valuation layers and account moves, then add branches for `property_valuation == 'perpetual_reception_invoicing'` in those methods.
