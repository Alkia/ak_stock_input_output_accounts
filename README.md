# AK Stock Input/Output Accounts Module for Odoo 19

## Overview
This module restores the **Stock Input Account** and **Stock Output Account** fields to Product Categories in Odoo 19, providing compatibility with workflows from previous Odoo versions.

**Author:** Alkia IT Services  
**Website:** https://www.alkia.net

## Why This Module?
In Odoo 19, the stock valuation system was redesigned and the separate Stock Input/Output accounts were removed from product categories. This module brings them back for users who:
- Are migrating from older Odoo versions
- Need separate GRNI (Goods Received Not Invoiced) tracking
- Want more granular control over interim stock accounts
- Have specific Anglo-Saxon accounting requirements

## Features
- ✅ Adds **Stock Input Account** field to product categories
- ✅ Adds **Stock Output Account** field to product categories  
- ✅ Creates journal entries immediately on receipt/delivery (not deferred to invoicing)
- ✅ Compatible with Perpetual (at invoicing) valuation method
- ✅ Compatible with Periodic (at closing) valuation method
- ✅ Respects company-specific configurations (multi-company ready)
- ✅ Integrates seamlessly with Odoo 19's new stock valuation system

## Installation

### Method 1: Manual Installation
1. Copy the `ak_stock_input_output_accounts` folder to your Odoo addons directory
2. Update the apps list: Go to Apps → Update Apps List
3. Search for "AK Stock Input/Output Accounts"
4. Click Install

### Method 2: Command Line
```bash
# Copy module to addons directory
cp -r ak_stock_input_output_accounts /path/to/odoo/addons/

# Restart Odoo
sudo systemctl restart odoo

# Install via command line
odoo-bin -d your_database -i ak_stock_input_output_accounts
```

## Configuration

### Step 1: Enable Automatic Accounting (if not already done)
1. Go to **Accounting → Configuration → Settings**
2. In the **Stock Valuation** section, enable **Automatic Accounting**
3. Choose your valuation method:
   - **Perpetual (at invoicing)** - for Anglo-Saxon accounting
   - **Periodic (at closing)** - for Continental accounting

### Step 2: Configure Product Category Accounts
1. Go to **Inventory → Configuration → Product Categories**
2. Select a category (e.g., "All / Saleable")
3. In the **Account Stock Properties** section, you'll now see:
   - **Stock Valuation Account** - Main inventory asset account
   - **Stock Input Account** - Interim account for incoming goods (GRNI)
   - **Stock Output Account** - Interim account for outgoing goods

### Step 3: Set Up the Accounts
Example configuration for Anglo-Saxon accounting:

| Field | Suggested Account | Account Type |
|-------|------------------|--------------|
| Stock Valuation Account | Stock Valuation / Inventory | Current Assets |
| Stock Input Account | Stock Interim (Received) / GRNI | Current Assets |
| Stock Output Account | Stock Interim (Delivered) | Current Assets |

**Note:** The Stock Input/Output accounts should typically be Current Assets accounts, even though they represent temporary positions.

## How It Works

### For Purchase Orders (Stock Input Account)

#### 1. Receive Products
When you validate the receipt of products, journal entries are created **immediately**:

**Journal Entry on Receipt:**
```
DEBIT:   Stock Valuation Account        $1,000  (increases inventory)
CREDIT:  Stock Input Account            $1,000  (temporary credit - GRNI)
```

This creates a "Goods Received Not Invoiced" (GRNI) situation where you have the inventory but haven't been billed yet.

#### 2. Validate Vendor Bill
When the vendor bill is posted, the interim account is cleared:

**Journal Entry on Bill:**
```
DEBIT:   Stock Input Account            $1,000  (clears the interim)
DEBIT:   Input VAT                         $70  (if applicable)
CREDIT:  Accounts Payable                $1,070  (liability to vendor)
```

**Net Result:** Inventory increased, liability to vendor recorded, interim account balanced.

#### ⚠️ CRITICAL: Handling Quantity Discrepancies

**Common Scenario:**
- Purchase Order: 100 units ordered
- Goods Receipt: 90 units actually received
- Question: What should the vendor bill show?

**Answer:** Bill MUST match receipt quantity (90 units), not PO quantity (100 units).

**How to do this correctly in Odoo:**
1. ✅ **Create Bill FROM the Receipt** (WH/IN/00011)
   - Click "Create Bill" button on the receipt
   - Odoo automatically populates bill qty = 90 (received qty)
   - GRNI = 90 THB (matches what was credited at receipt)

2. ❌ **DON'T Create Bill from PO**
   - Would default to 100 units
   - Creates GRNI mismatch (90 credited, 100 debited)
   - Accounting discrepancy!

**Example Flow:**
```
Step 1: PO P00018 - Order 100 units @ 1 THB = 100 THB
        → No accounting entry

Step 2: Receipt WH/IN/00011 - Receive 90 units
        → Dr Inventory 90 / Cr GRNI 90

Step 3: Create Bill FROM Receipt - Bill shows 90 units
        → Dr GRNI 90 / Dr VAT 6.30 / Cr AP 96.30
        → GRNI balance = 0 ✅

Remaining 10 units:
        → Either receive later (new receipt + bill)
        → Or cancel on PO
```

See **CASE_STUDY.md** for detailed explanation and scenarios.

---

### For Sales Orders (Stock Output Account)

#### 1. Deliver Products
When you validate the delivery, journal entries are created **immediately**:

**Journal Entry on Delivery:**
```
DEBIT:   Stock Output Account            $800  (temporary debit)
CREDIT:  Stock Valuation Account         $800  (reduces inventory)
```

This creates a "Goods Shipped Not Invoiced" situation where you've sent the goods but haven't invoiced yet.

#### 2. Create Customer Invoice
When the customer invoice is posted, the interim account is cleared:

**Journal Entry on Invoice:**
```
DEBIT:   Accounts Receivable            $1,200  (asset from customer)
CREDIT:  Revenue Account                $1,200  (income)

DEBIT:   Cost of Goods Sold              $800  (expense)
CREDIT:  Stock Output Account            $800  (clears the interim)
```

**Net Result:** Revenue recorded, COGS posted, receivable created, interim account balanced.

---

## Key Differences from Odoo 19 Standard Behavior

### Odoo 19 Standard (without this module):
- Journal entries created **only when invoice/bill is posted**
- No interim accounts used
- Direct posting to COGS or Stock Valuation

### With AK Module:
- Journal entries created **on receipt/delivery** (physical movement)
- Uses interim accounts (Stock Input/Output)
- Provides better tracking of GRNI and goods in transit
- Matches traditional Anglo-Saxon accounting more closely

## Accounting Flow Diagrams

### Purchase Flow
```
Receipt → Stock Valuation ↑ / Stock Input ↓ (GRNI created)
Bill    → Stock Input ↑ / Accounts Payable ↓ (GRNI cleared)
```

### Sales Flow
```
Delivery → Stock Output ↑ / Stock Valuation ↓ (goods shipped)
Invoice  → Accounts Receivable ↑ / Revenue ↑
           COGS ↑ / Stock Output ↓ (interim cleared)
```

## Differences from Previous Odoo Versions

### Odoo 16-18
- Stock movements created real-time journal entries
- Separate valuation layers were created for each move
- Stock Input/Output accounts were used for every stock move

### Odoo 19 (with this module)
- Journal entries are created on receipt/delivery (physical movement)
- Valuation data is stored directly on stock moves (no separate layers)
- Stock Input/Output accounts track interim positions
- Performance is improved with streamlined data structure

## Compatibility with Odoo 19 Features

This module is fully compatible with:
- ✅ New Stock Valuation report (Accounting → Review → Inventory Valuation)
- ✅ Periodic closing entries
- ✅ Average Cost (AVCO) costing method
- ✅ FIFO costing method
- ✅ Standard Cost costing method
- ✅ Multi-company operations
- ✅ Multi-currency operations

## Use Cases

### When to Use This Module
- **GRNI Tracking:** You need to track goods received but not yet invoiced
- **Cash Flow Analysis:** You want to see inventory liability before bills arrive
- **Audit Requirements:** Your auditors require separate interim accounts
- **Migration:** You're upgrading from older Odoo versions
- **ERP Integration:** Your external systems expect these interim accounts

### When Standard Odoo 19 is Sufficient
- Simple business operations
- You don't need GRNI tracking
- Immediate invoicing after receipt/delivery
- Simplified accounting structure preferred

## Troubleshooting

### Accounts Not Showing
- Ensure you have "Show Full Accounting Features" enabled for your user
- Go to Settings → Users → (your user) → Enable "Show Full Accounting Features"
- Activate Developer Mode if needed

### Fields Not Visible in Product Category
- Install the module
- Refresh your browser (Ctrl+F5)
- Check that you're editing a product category, not a product

### Journal Entries Not Created on Receipt
- Verify Automatic Accounting is enabled (Accounting → Settings)
- Check that property_valuation is set to 'real_time' on the category
- Ensure the Stock Input Account is configured on the category
- Verify the product uses automated inventory valuation

### Journal Entries Not Created on Delivery
- Same checks as above
- Ensure the Stock Output Account is configured
- Verify the delivery is for a product with real-time valuation

### Double Entries or Missing Entries
- Check if Anglo-Saxon accounting is enabled
- Verify your valuation method (Perpetual vs Periodic)
- Review the Stock Journal for all entries
- Use Developer Mode to check stock.move records

## Technical Details

### Models Extended
- `product.category` - Adds the two account fields
- `stock.move` - Creates journal entries on validation, uses the accounts during valuation
- `stock.valuation.layer` - Ensures entries are created at the right time
- `account.move` - Clears interim accounts when invoices/bills are posted

### Key Methods Overridden
- `_get_accounting_data_for_valuation()` - Returns the Stock Input/Output accounts
- `_prepare_account_move_line()` - Uses the correct accounts for journal entries
- `_stock_account_prepare_anglo_saxon_in_lines_vals()` - Clears Stock Input Account on bill
- `_stock_account_prepare_anglo_saxon_out_lines_vals()` - Clears Stock Output Account on invoice

### Dependencies
- `stock_account` (Odoo standard module)

### Database Changes
- Adds two property fields (company-dependent)
- No migration required for existing data
- Safe to install/uninstall

## Support & Contributing
This is a module by **Alkia IT Services**.

For support:
- Visit: https://www.alkia.net
- Email: support@alkia.net

Feel free to:
- Report issues
- Suggest improvements  
- Request customizations

## License
LGPL-3

## Credits
**Developed by:** Alkia IT Services  
**Purpose:** Bridge the gap between Odoo 19's redesigned stock valuation and traditional Anglo-Saxon accounting workflows.

---

**Version:** 19.0.1.0.0  
**Last Updated:** 2025
