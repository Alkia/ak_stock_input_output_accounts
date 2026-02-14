# AK Stock Input/Output Accounts - Quick Installation Guide

## Module Information
- **Name:** AK Stock Input/Output Accounts
- **Technical Name:** ak_stock_input_output_accounts
- **Version:** 19.0.1.0.0
- **Author:** Alkia IT Services
- **Website:** https://www.alkia.net
- **License:** LGPL-3

## What This Module Does

This module adds **Stock Input Account** and **Stock Output Account** fields back to Product Categories in Odoo 19.

### Key Behavior:
- **On Product Receipt:** Creates journal entry immediately (DEBIT Stock Valuation, CREDIT Stock Input)
- **On Vendor Bill:** Clears interim account (DEBIT Stock Input, CREDIT Accounts Payable)
- **On Delivery:** Creates journal entry immediately (DEBIT Stock Output, CREDIT Stock Valuation)
- **On Customer Invoice:** Clears interim account (DEBIT COGS, CREDIT Stock Output)

This provides **GRNI (Goods Received Not Invoiced)** tracking and better cash flow visibility.

## Installation Steps

### 1. Copy Module to Addons Directory
```bash
# Copy the ak_stock_input_output_accounts folder to your Odoo addons directory
cp -r ak_stock_input_output_accounts /opt/odoo/addons/
# OR your custom addons path
cp -r ak_stock_input_output_accounts /path/to/your/addons/
```

### 2. Set Correct Permissions
```bash
sudo chown -R odoo:odoo /opt/odoo/addons/ak_stock_input_output_accounts
sudo chmod -R 755 /opt/odoo/addons/ak_stock_input_output_accounts
```

### 3. Update Odoo Addons Path (if needed)
Make sure your `odoo.conf` includes the addons directory:
```ini
[options]
addons_path = /opt/odoo/addons,/opt/odoo/enterprise,/path/to/custom/addons
```

### 4. Restart Odoo Service
```bash
sudo systemctl restart odoo
# OR
sudo service odoo restart
```

### 5. Update Apps List in Odoo
1. Log in to Odoo as Administrator
2. Enable Developer Mode:
   - Go to Settings
   - Scroll to bottom
   - Click "Activate the developer mode"
3. Go to **Apps** menu
4. Click **Update Apps List** (top menu or three dots)
5. Click **Update** in the dialog

### 6. Install the Module
1. In Apps menu, remove the "Apps" filter
2. Search for "AK Stock" or "Stock Input Output"
3. Find "AK Stock Input/Output Accounts" 
4. Click **Install**

### 7. Configure Accounts
1. Go to **Inventory → Configuration → Product Categories**
2. Select a category (e.g., "All / Saleable")
3. Set these accounts:
   - **Stock Valuation Account:** Your main inventory asset account
   - **Stock Input Account:** Interim account for GRNI (e.g., "Stock Interim - Received")
   - **Stock Output Account:** Interim account for shipped goods (e.g., "Stock Interim - Delivered")

### 8. Enable Automatic Accounting (if not already)
1. Go to **Accounting → Configuration → Settings**
2. Enable **Automatic Accounting**
3. Choose **Perpetual (at invoicing)** for Anglo-Saxon accounting

## Creating Interim Accounts

If you don't have interim accounts yet, create them:

### Stock Input Account (GRNI)
1. Go to **Accounting → Configuration → Chart of Accounts**
2. Click **Create**
3. Fill in:
   - **Code:** 1151 (or your preferred code)
   - **Account Name:** Stock Interim - Received (GRNI)
   - **Type:** Current Assets
   - **Reconcile:** Yes (recommended)

### Stock Output Account
1. Click **Create** again
2. Fill in:
   - **Code:** 1152 (or your preferred code)
   - **Account Name:** Stock Interim - Delivered
   - **Type:** Current Assets
   - **Reconcile:** Yes (recommended)

## Testing the Module

### Test Purchase Flow:
1. Create a Purchase Order with a product
2. **Receive the products** - Check Journal Entry (should show Stock Valuation DEBIT, Stock Input CREDIT)
3. **Create and post Vendor Bill FROM THE RECEIPT** - Check Journal Entry (should show Stock Input DEBIT, Accounts Payable CREDIT)
4. Verify Stock Input Account balance is zero

### Test Sales Flow:
1. Create a Sales Order with a product
2. **Deliver the products** - Check Journal Entry (should show Stock Output DEBIT, Stock Valuation CREDIT)
3. **Create and post Customer Invoice** - Check Journal Entry (should show COGS DEBIT, Stock Output CREDIT)
4. Verify Stock Output Account balance is zero

### ⚠️ Important: Quantity Discrepancies
**Always create vendor bills FROM the receipt, not from the Purchase Order.**

Example: If PO = 100 units but you received only 90 units:
- Go to the Receipt (WH/IN/00011)
- Click "Create Bill"
- Bill will automatically show 90 units (correct!)
- GRNI will clear properly (90 THB)

See **CASE_STUDY.md** for detailed explanation of this critical scenario.

## Verification

### Check Journal Entries:
- Go to **Accounting → Accounting → Journal Entries**
- Filter by "Stock Journal"
- Look for entries with your Stock Input/Output accounts

### Check Account Balances:
- Go to **Accounting → Reporting → General Ledger**
- Find your Stock Input and Stock Output accounts
- They should show transactions when goods are in transit
- They should balance to zero when invoices/bills are posted

## Troubleshooting

### Module Not Appearing in Apps List
- Verify the folder is in the correct addons path
- Check file permissions (should be readable by Odoo user)
- Restart Odoo service
- Update Apps List again

### Fields Not Showing on Product Category
- Clear browser cache (Ctrl+F5)
- Enable Developer Mode
- Check you have accounting access rights
- Verify the module is installed (should show "Installed" in Apps)

### Journal Entries Not Created
- Check that Automatic Accounting is enabled
- Verify the product category has property_valuation = 'real_time'
- Ensure the Stock Input/Output accounts are set on the category
- Check that you're using a stockable product (not service/consumable)

### Wrong Accounts in Journal Entries
- Double-check the accounts configured on the product category
- Verify the product is assigned to the correct category
- Check if there are location-specific account overrides

## Uninstallation

If you need to uninstall the module:

1. Go to **Apps**
2. Remove "Apps" filter
3. Search for "AK Stock"
4. Click the three dots → **Uninstall**
5. Confirm uninstallation

**Note:** The Stock Input/Output account fields will be removed, but existing journal entries will remain.

## Support

**Developed by:** Alkia IT Services  
**Website:** https://www.alkia.net  
**Email:** support@alkia.net

For technical support or customization requests, please contact Alkia IT Services.

## Additional Resources

- Full documentation: See README.md
- Odoo documentation: https://www.odoo.com/documentation/19.0/
- Accounting module docs: https://www.odoo.com/documentation/19.0/applications/finance/accounting.html

---

**Last Updated:** February 2025  
**Module Version:** 19.0.1.0.0