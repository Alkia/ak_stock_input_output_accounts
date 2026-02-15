<!--
################################################################################
# Module:        Stock Input/Output Accounts Module for Odoo 19                   
# Version:       19.0.2                              
# Last Updated:  2026-01-04                          
# Author:        M
# Company:       Alkia IT Services Co., Ltd.
# Location:      Khet Khlong Toei, Krung Thep Maha Nakhon, TH
# Copyright (c): 2025-Now Alkia IT Services Co., Ltd.
# License:       Proprietary (see LICENSE file)
# Dependencies:  Python 3.12+, Odoo 19+              
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
# You should have received a copy of the License along with this program.
# If not, refer to https://www.alkia.net/license
#################################################################################
-->

# VISUAL ACCOUNTING FLOWS
## AK Stock Input/Output Accounts Module

---

## PURCHASE FLOW - STANDARD CASE (No Quantity Discrepancy)

```
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: PURCHASE ORDER (P00018)                                    │
│ Order: 100 units @ 1 THB = 100 THB                                 │
├─────────────────────────────────────────────────────────────────────┤
│ Business Impact:  Commitment created                                │
│ Accounting Impact: NONE                                             │
│ Status:          PO open for 100 units                              │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: GOODS RECEIPT (WH/IN/00011)                                │
│ Receive: 100 units @ 1 THB = 100 THB                               │
├─────────────────────────────────────────────────────────────────────┤
│ Journal Entry:                                                      │
│   Dr 130000 Inventory                    100.00                     │
│   Cr 231001 GRNI                                  100.00            │
├─────────────────────────────────────────────────────────────────────┤
│ Balance Sheet:                                                      │
│   Inventory:  +100                                                  │
│   GRNI:       +100 (liability)                                      │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: VENDOR BILL (Created from Receipt)                         │
│ Bill: 100 units @ 1 THB + 7% VAT = 107 THB                         │
├─────────────────────────────────────────────────────────────────────┤
│ Journal Entry:                                                      │
│   Dr 231001 GRNI                         100.00                     │
│   Dr 140003 Input VAT                      7.00                     │
│   Cr 210002 Accounts Payable                      107.00            │
├─────────────────────────────────────────────────────────────────────┤
│ Balance Sheet:                                                      │
│   GRNI:       0 (100 - 100)              ✅ CLEARED                 │
│   Input VAT:  +7 (recoverable)                                      │
│   AP:         +107 (liability to vendor)                            │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: PAYMENT                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Journal Entry:                                                      │
│   Dr 210002 Accounts Payable            107.00                      │
│   Cr 190001 Outstanding Payment                   107.00            │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 5: BANK RECONCILIATION                                         │
├─────────────────────────────────────────────────────────────────────┤
│ Journal Entry:                                                      │
│   Dr 190001 Outstanding Payment          107.00                     │
│   Cr 110101 Bank Account                          107.00            │
└─────────────────────────────────────────────────────────────────────┘

Final Balances:
  Inventory:   +100
  Input VAT:   +7
  Bank:        -107
  GRNI:        0 ✅
  AP:          0 ✅
```

---

## PURCHASE FLOW - QUANTITY DISCREPANCY (THE CRITICAL CASE)

```
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: PURCHASE ORDER (P00018)                                    │
│ Order: 100 units @ 1 THB = 100 THB                                 │
├─────────────────────────────────────────────────────────────────────┤
│ Business Impact:  Commitment for 100 units                          │
│ Accounting Impact: NONE                                             │
│ Status:          PO open for 100 units                              │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: GOODS RECEIPT (WH/IN/00011)                                │
│ Receive: 90 units @ 1 THB = 90 THB  ⚠️ LESS THAN ORDERED           │
├─────────────────────────────────────────────────────────────────────┤
│ Journal Entry:                                                      │
│   Dr 130000 Inventory                     90.00                     │
│   Cr 231001 GRNI                                   90.00            │
├─────────────────────────────────────────────────────────────────────┤
│ Balance Sheet:                                                      │
│   Inventory:  +90                                                   │
│   GRNI:       +90 (liability)                                       │
│                                                                     │
│ PO Status:    90 received / 10 to receive                           │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   CRITICAL DECISION     │
              │   CREATE BILL FROM:     │
              └─────────────────────────┘
                     │            │
          ✅ CORRECT │            │ ❌ WRONG
        ┌────────────┘            └────────────┐
        ▼                                      ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│ FROM RECEIPT             │      │ FROM PURCHASE ORDER      │
│ (WH/IN/00011)            │      │ (P00018)                 │
├──────────────────────────┤      ├──────────────────────────┤
│ Bill Qty: 90 units ✅    │      │ Bill Qty: 100 units ❌   │
│ Amount: 90 + 6.30 VAT    │      │ Amount: 100 + 7.00 VAT   │
│ Total: 96.30 THB         │      │ Total: 107.00 THB        │
└──────────────────────────┘      └──────────────────────────┘
        │                                      │
        ▼                                      ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│ JOURNAL ENTRY:           │      │ JOURNAL ENTRY:           │
│                          │      │                          │
│ Dr 231001 GRNI    90.00  │      │ Dr 231001 GRNI   100.00  │
│ Dr 140003 VAT      6.30  │      │ Dr 140003 VAT      7.00  │
│ Cr 210002 AP      96.30  │      │ Cr 210002 AP     107.00  │
│                          │      │                          │
│ GRNI Balance: 0 ✅       │      │ GRNI Balance: -10 ❌     │
│ (90 - 90 = 0)            │      │ (90 - 100 = -10)         │
│                          │      │                          │
│ Result: CORRECT          │      │ Result: MISMATCH!        │
└──────────────────────────┘      └──────────────────────────┘
```

---

## WHAT HAPPENS TO THE REMAINING 10 UNITS?

### Option A: Supplier Delivers Later
```
Current State:
  PO P00018:     100 ordered / 90 received / 10 to receive
  GRNI:          0 (cleared)
  Inventory:     90

Remaining 10 Units Arrive:
  ┌─────────────────────────────────┐
  │ NEW RECEIPT (WH/IN/00012)       │
  │ Receive: 10 units               │
  ├─────────────────────────────────┤
  │ Dr Inventory          10.00     │
  │ Cr GRNI                   10.00 │
  └─────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────┐
  │ NEW BILL FROM RECEIPT           │
  │ Bill: 10 units + VAT            │
  ├─────────────────────────────────┤
  │ Dr GRNI               10.00     │
  │ Dr Input VAT           0.70     │
  │ Cr AP                     10.70 │
  └─────────────────────────────────┘

Final State:
  Inventory:     100 ✅
  GRNI:          0 ✅
```

### Option B: Cancel Remaining Quantity
```
Current State:
  PO P00018:     100 ordered / 90 received / 10 to receive
  
Action: Update PO
  Set delivered qty = 90
  PO status: Fully Received
  
No Additional Accounting Entries Needed
  
Final State:
  Inventory:     90 (final)
  GRNI:          0 ✅
```

---

## SALES FLOW (For Completeness)

```
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: SALES ORDER                                                 │
│ Sell: 50 units @ 2 THB = 100 THB                                   │
├─────────────────────────────────────────────────────────────────────┤
│ Accounting Impact: NONE                                             │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: DELIVERY VALIDATION                                         │
│ Deliver: 50 units (cost: 50 @ 1 THB = 50 THB)                      │
├─────────────────────────────────────────────────────────────────────┤
│ Journal Entry:                                                      │
│   Dr Stock Output Account            50.00                          │
│   Cr 130000 Inventory                        50.00                  │
├─────────────────────────────────────────────────────────────────────┤
│ Balance Sheet:                                                      │
│   Inventory:      -50 (reduced)                                     │
│   Stock Output:   +50 (interim asset)                               │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: CUSTOMER INVOICE                                            │
│ Invoice: 50 units @ 2 THB + 7% VAT = 107 THB                       │
├─────────────────────────────────────────────────────────────────────┤
│ Journal Entries (combined):                                         │
│   Dr Accounts Receivable             107.00                         │
│   Cr Revenue                                 100.00                 │
│   Cr Output VAT                                7.00                 │
│                                                                     │
│   Dr Cost of Goods Sold               50.00                         │
│   Cr Stock Output Account                    50.00                  │
├─────────────────────────────────────────────────────────────────────┤
│ Balance Sheet:                                                      │
│   Stock Output:   0 (50 - 50)       ✅ CLEARED                      │
│   AR:            +107                                               │
│   Revenue:       +100                                               │
│   COGS:          +50 (expense)                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ACCOUNT FLOW SUMMARY

### Thai Chart of Accounts
```
ASSETS:
  110101 Bank Account                  เงินฝากธนาคาร
  130000 Inventory                     สินค้าคงเหลือ
  140003 Input VAT                     ภาษีซื้อรอเรียกคืน
  190001 Outstanding Payment           เงินจ่ายรอตัดบัญชี
  Accounts Receivable                  ลูกหนี้การค้า

LIABILITIES:
  210002 Accounts Payable              เจ้าหนี้การค้าในประเทศ
  231001 GRNI                          สินค้ารับแล้วยังไม่ได้รับใบแจ้งหนี้
  Output VAT                           ภาษีขายรอนำส่ง

EQUITY/P&L:
  Revenue                              รายได้
  Cost of Goods Sold                   ต้นทุนขาย
```

### Account Movement Flow
```
PURCHASE:
  Receipt:  Inventory ↑ / GRNI ↑
  Bill:     GRNI ↓ / AP ↑ / Input VAT ↑
  Payment:  AP ↓ / Bank ↓

SALES:
  Delivery: Stock Output ↑ / Inventory ↓
  Invoice:  AR ↑ / Revenue ↑ / Output VAT ↑
            COGS ↑ / Stock Output ↓
```

---

## KEY RECONCILIATION POINTS

### After Each Purchase:
```
✅ GRNI should return to ZERO after bill is posted
✅ Inventory should equal received quantity × cost
✅ AP should equal bill total (including VAT)
```

### After Each Sale:
```
✅ Stock Output should return to ZERO after invoice
✅ Inventory reduced by delivered quantity × cost
✅ COGS should equal inventory reduction
```

---

**Module:** ak_stock_input_output_accounts  
**Author:** Alkia IT Services  
**Version:** 19.0.1.0.0
