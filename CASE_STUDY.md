# CASE STUDY: PO Quantity vs Receipt Quantity Discrepancy

## Module: AK Stock Input/Output Accounts
## Author: Alkia IT Services

---

## THE PROBLEM

**Scenario:**
- Purchase Order created: **100 units** @ 1 THB = 100 THB
- Actual goods received: **90 units** @ 1 THB = 90 THB
- Question: How should the vendor bill and GRNI be handled?

**Critical Question:**
> If the Bill is generated from the PO, there is a problem: quantity = 100 in the PO instead of Quantity = 90 at the reception. How is this fixed?

---

## THE SOLUTION IN ODOO

### Key Principle
**ALWAYS create the vendor bill from the RECEIPT, not from the Purchase Order.**

This ensures that:
1. Bill quantity matches actual received quantity (90 units)
2. GRNI clearing matches what was credited (90 THB)
3. No accounting discrepancy occurs

### Correct Workflow in Odoo

#### Step 1: Purchase Order (P00018)
- **Ordered:** 100 units @ 1 THB = 100 THB
- **Accounting Impact:** NONE
- **Status:** PO remains open for remaining 10 units

```
Account                          Debit    Credit
—                                —        —
(No entry at PO confirmation)
```

#### Step 2: Goods Receipt (WH/IN/00011)
- **Received:** 90 units @ 1 THB = 90 THB
- **Accounting Impact:** Create GRNI for actual received value

```
Journal Entry:
Account                          Debit    Credit
130000 Inventory                 90.00
231001 GRNI                               90.00
```

**Why 90 THB?**
- We received only 90 units
- Inventory increases by actual received quantity
- GRNI liability = 90 THB (not 100 THB from PO)

#### Step 3: Create Vendor Bill FROM THE RECEIPT
**CRITICAL:** Click "Create Bill" button on the receipt (WH/IN/00011), NOT from the PO.

When creating bill from receipt:
- **Bill Quantity:** Automatically populated as **90 units** ✅
- **Bill Amount (excluding VAT):** 90 THB
- **VAT (7%):** 6.30 THB
- **Total Payable:** 96.30 THB

```
Journal Entry on Bill Posting:
Account                          Debit    Credit
231001 GRNI                      90.00
140003 Input VAT                 6.30
210002 Accounts Payable                   96.30
```

**Result:**
- GRNI balance = 0 (90 credit - 90 debit)
- AP balance = 96.30 THB
- Inventory remains at 90 THB

#### Step 4: Payment
```
Journal Entry:
Account                          Debit    Credit
210002 Accounts Payable          96.30
190001 Outstanding Payment                96.30
```

#### Step 5: Bank Reconciliation
```
Journal Entry:
Account                          Debit    Credit
190001 Outstanding Payment       96.30
110101 Bank Account                       96.30
```

---

## WHAT ABOUT THE REMAINING 10 UNITS?

The Purchase Order (P00018) shows:
- **Ordered:** 100 units
- **Received:** 90 units
- **Remaining:** 10 units

### Options:

### Option A: Receive Later
If the remaining 10 units arrive later:
1. Create a new receipt from the same PO
2. Receive 10 units
3. New GRNI entry: Dr Inventory 10 / Cr GRNI 10
4. Create bill from this second receipt for 10 units
5. Clear GRNI: Dr GRNI 10 / Cr AP 10.70 (with VAT)

### Option B: Cancel the Remaining Quantity
If supplier won't deliver the remaining 10 units:
1. Go to Purchase Order P00018
2. Click on the product line
3. Set "Delivered Qty" = 90 (update the PO)
4. The PO will show as fully received
5. No further GRNI or accounting impact

### Option C: Price Discount Instead
If supplier gives a 10% discount for the shortage:
1. Receive all 90 units (GRNI = 90)
2. When creating bill, manually adjust price
3. Bill total = 81 THB (90 units @ 0.90 THB each)
4. GRNI clearing entry will be different:
   - Dr GRNI 90
   - Cr Inventory 9 (price variance)
   - Dr Input VAT 5.67
   - Cr AP 86.67

---

## WHY THIS WORKS IN ODOO v16+

### Automatic Quantity Matching
When you click "Create Bill" from a receipt:
- Odoo automatically populates bill qty = received qty
- No manual intervention needed
- Prevents over-billing

### Receipt-to-Bill Linkage
```
PO (100) → Receipt (90) → Bill (90) ✅
PO (100) → Bill (100) ❌ WRONG - creates GRNI mismatch
```

### Visual Confirmation
In the Purchase Order form:
- **To Invoice:** Shows only received quantity (90)
- **Billed:** Shows what has been invoiced
- **Remaining:** Shows unbilled received quantity

---

## ACCOUNTING BALANCES AT EACH STAGE

### After Receipt (WH/IN/00011)
```
130000 Inventory:        90.00 DR
231001 GRNI:            90.00 CR
```

### After Bill Posted
```
130000 Inventory:        90.00 DR
231001 GRNI:             0.00 (90 CR - 90 DR)
140003 Input VAT:        6.30 DR
210002 AP:              96.30 CR
```

### After Payment
```
130000 Inventory:        90.00 DR
140003 Input VAT:        6.30 DR
190001 Outstanding:      0.00 (96.30 CR - 96.30 DR)
210002 AP:               0.00 (96.30 CR - 96.30 DR)
110101 Bank:            96.30 CR
```

---

## COMMON MISTAKES TO AVOID

### ❌ Mistake 1: Creating Bill from PO
**Don't:**
```
Purchase → P00018 → Create Bill → 100 units
```

**This creates:**
- Bill for 100 THB
- But GRNI is only 90 THB
- 10 THB discrepancy!

### ❌ Mistake 2: Manual Bill Entry
**Don't:**
- Create bill from Accounting → Vendor Bills → Create
- Manually enter 90 units
- Try to link to PO

**Why not?**
- May not properly link to receipt
- GRNI may not clear correctly
- Audit trail is broken

### ✅ Correct Method
```
Inventory → Receipts → WH/IN/00011 → Create Bill
```
This ensures:
- Quantity auto-populated from receipt
- GRNI clearing is automatic
- Full audit trail maintained

---

## ODOO CONFIGURATION CHECKLIST

To ensure this works correctly:

### 1. Enable Automatic Accounting
- Go to **Accounting → Configuration → Settings**
- Enable **Automatic Accounting**
- Choose **Perpetual (at invoicing)**

### 2. Configure Product Category
- Go to **Inventory → Configuration → Product Categories**
- Select category (e.g., "All / Saleable")
- Set accounts:
  - **Stock Valuation Account:** 130000 Inventory
  - **Stock Input Account (GRNI):** 231001 GRNI
  - **Stock Output Account:** (for sales)

### 3. Product Configuration
- Product type: **Storable Product**
- Costing method: **Average Cost (AVCO)** or **FIFO**
- Inventory Valuation: **Automated**

### 4. Install AK Module
- Install **ak_stock_input_output_accounts**
- This ensures GRNI account is used correctly

---

## VERIFICATION STEPS

### Test the Flow:

1. **Create PO for 100 units**
   - Check: No journal entry

2. **Receive only 90 units**
   - Go to Accounting → Journal Entries
   - Find the stock journal entry
   - Verify: Dr Inventory 90 / Cr GRNI 90

3. **Create Bill from Receipt**
   - Click "Create Bill" on WH/IN/00011
   - Verify: Bill shows 90 units (not 100)
   - Post the bill
   - Check journal entry
   - Verify: Dr GRNI 90 / Dr VAT 6.30 / Cr AP 96.30

4. **Check GRNI Balance**
   - Go to Accounting → Chart of Accounts
   - Find 231001 GRNI
   - Balance should be: **0.00** ✅

---

## THAI ACCOUNTING CONTEXT

### Chart of Accounts Mapping
```
130000 สินค้าคงเหลือ (Inventory)
231001 สินค้ารับแล้วยังไม่ได้รับใบแจ้งหนี้ (GRNI)
140003 ภาษีซื้อรอเรียกคืน (Input VAT)
210002 เจ้าหนี้การค้าในประเทศ (Accounts Payable)
190001 เงินจ่ายรอตัดบัญชี (Outstanding Payment)
110101 เงินฝากธนาคาร (Bank Account)
```

### VAT Handling
- Standard VAT rate: 7%
- Input VAT is recoverable
- Calculated on actual invoiced amount (90 THB, not 100 THB)

---

## SUMMARY

### The Rule
**Bill Quantity MUST Match Receipt Quantity**

### The Method
**Always Create Bill FROM the Receipt, Never FROM the PO**

### The Result
- GRNI clears to zero
- No accounting discrepancies
- Proper audit trail
- Correct VAT amount

### What Odoo v16+ Does Automatically
1. Links bill to receipt (not PO)
2. Populates bill qty = receipt qty
3. Clears GRNI for exact receipt amount
4. Handles quantity discrepancies gracefully

---

**Module:** ak_stock_input_output_accounts  
**Author:** Alkia IT Services  
**Version:** 19.0.1.0.0  
**Last Updated:** February 2025
