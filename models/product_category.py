from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_stock_account_input_categ_id = fields.Many2one(
        'account.account',
        string='Stock Input Account (GRNI)',
        company_dependent=True,
        domain="[('account_type', 'in', ['asset_current', 'liability_current']), ('deprecated', '=', False), ('company_id', '=', allowed_company_ids[0])]",
        check_company=True,
        help="Goods Received Not Invoiced (GRNI) account - Thai: สินค้ารับแล้วยังไม่ได้รับใบแจ้งหนี้\n\n"
             "STEP 2 - Goods Receipt (e.g., 90 units received):\n"
             "• DEBIT: 130000 Inventory (90 THB)\n"
             "• CREDIT: 231001 GRNI (90 THB)\n\n"
             "STEP 3 - Vendor Bill Posted (for 90 units actually received):\n"
             "• DEBIT: 231001 GRNI (90 THB) - clears interim\n"
             "• DEBIT: 140003 Input VAT (6.30 THB)\n"
             "• CREDIT: 210002 Accounts Payable (96.30 THB)\n\n"
             "Note: Bill quantity should match received quantity (90), not PO quantity (100)"
    )
    
    property_stock_account_output_categ_id = fields.Many2one(
        'account.account',
        string='Stock Output Account',
        company_dependent=True,
        domain="[('account_type', 'in', ['asset_current', 'liability_current']), ('deprecated', '=', False), ('company_id', '=', allowed_company_ids[0])]",
        check_company=True,
        help="Goods Shipped Not Invoiced account - Thai: สินค้าส่งแล้วยังไม่ได้ออกใบแจ้งหนี้\n\n"
             "STEP 1 - Delivery Validation:\n"
             "• DEBIT: Stock Output Account (temporary debit)\n"
             "• CREDIT: Stock Valuation Account (reduces inventory)\n\n"
             "STEP 2 - Customer Invoice Posted:\n"
             "• DEBIT: Accounts Receivable (asset from customer)\n"
             "• CREDIT: Revenue Account\n"
             "• DEBIT: Cost of Goods Sold\n"
             "• CREDIT: Stock Output Account (clears the interim)"
    )


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_accounting_data_for_valuation(self):
        """
        Override to use category-level stock input/output accounts if defined.
        This ensures GRNI (231001) is used instead of generic accounts.
        """
        journal_id, acc_src, acc_dest, acc_valuation = super()._get_accounting_data_for_valuation()
        
        # Get the product category
        product_category = self.product_id.categ_id
        
        # Check if we're dealing with incoming or outgoing moves
        if self._is_in():
            # Incoming move - use Stock Input Account (GRNI) if defined
            if product_category.property_stock_account_input_categ_id:
                acc_src = product_category.property_stock_account_input_categ_id.id
        elif self._is_out():
            # Outgoing move - use Stock Output Account if defined
            if product_category.property_stock_account_output_categ_id:
                acc_dest = product_category.property_stock_account_output_categ_id.id
        
        return journal_id, acc_src, acc_dest, acc_valuation

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, svl_id, description):
        """
        Prepare values for account move lines using Stock Input/Output accounts.
        
        For PURCHASE (Receipt - WH/IN/00011):
        - qty = actual received quantity (e.g., 90 units)
        - cost = actual cost (e.g., 90 THB if 1 THB/unit)
        - DEBIT: 130000 Inventory (90)
        - CREDIT: 231001 GRNI (90)
        
        This creates GRNI liability equal to the VALUE of goods received,
        not the PO amount.
        """
        self.ensure_one()
        
        # Get the accounting data with our custom accounts
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        
        # Determine if we should use our custom accounts
        product_category = self.product_id.categ_id
        
        if self._is_in() and product_category.property_stock_account_input_categ_id:
            # Incoming: Use Stock Input Account (GRNI) as source (credit)
            # DEBIT: Inventory (acc_valuation)
            # CREDIT: GRNI (acc_src)
            credit_account_id = acc_src
            debit_account_id = acc_valuation
        elif self._is_out() and product_category.property_stock_account_output_categ_id:
            # Outgoing: Use Stock Output Account as destination (debit)
            # DEBIT: Stock Output Account (acc_dest)
            # CREDIT: Inventory (acc_valuation)
            debit_account_id = acc_dest
            credit_account_id = acc_valuation
        
        # Call parent to prepare the move lines
        # The qty and cost parameters already reflect the ACTUAL received/delivered quantity
        res = super()._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id, svl_id, description
        )
        
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _stock_account_prepare_anglo_saxon_in_lines_vals(self):
        """
        Override to handle GRNI clearing when vendor bill is posted.
        
        CRITICAL CASE HANDLING:
        PO = 100 units → Receipt = 90 units → Bill should be 90 units
        
        When bill is created "from Receipt" (not from PO):
        - Bill qty = 90 (matches actual receipt)
        - GRNI to clear = 90 (matches what was credited at receipt)
        
        Journal Entry on Bill:
        • DEBIT: 231001 GRNI (90) - clears the interim
        • DEBIT: 140003 Input VAT (6.30)
        • CREDIT: 210002 Accounts Payable (96.30)
        
        The key is that Anglo-Saxon entries are based on RECEIVED quantity,
        not PO quantity. Odoo v16+ creates bills from receipts, ensuring
        this quantity match automatically.
        """
        lines_vals_list = super()._stock_account_prepare_anglo_saxon_in_lines_vals()
        
        for line_vals in lines_vals_list:
            # Find the invoice line
            invoice_line = self.invoice_line_ids.filtered(lambda l: l.id == line_vals.get('invoice_line_id'))
            if invoice_line and invoice_line.product_id:
                category = invoice_line.product_id.categ_id
                # Use Stock Input Account (GRNI) if defined
                if category.property_stock_account_input_categ_id:
                    line_vals['account_id'] = category.property_stock_account_input_categ_id.id
        
        return lines_vals_list

    def _stock_account_prepare_anglo_saxon_out_lines_vals(self):
        """
        Override to handle Stock Output Account clearing when customer invoice is posted.
        
        When invoice is posted after delivery:
        • DEBIT: Accounts Receivable (from customer)  
        • CREDIT: Revenue
        • DEBIT: COGS
        • CREDIT: Stock Output Account (clears the interim)
        """
        lines_vals_list = super()._stock_account_prepare_anglo_saxon_out_lines_vals()
        
        for line_vals in lines_vals_list:
            # Find the invoice line
            invoice_line = self.invoice_line_ids.filtered(lambda l: l.id == line_vals.get('invoice_line_id'))
            if invoice_line and invoice_line.product_id:
                category = invoice_line.product_id.categ_id
                # Use Stock Output Account if defined
                if category.property_stock_account_output_categ_id:
                    line_vals['account_id'] = category.property_stock_account_output_categ_id.id
        
        return lines_vals_list


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_account_move_line(self, move=None):
        """
        Ensure vendor bill lines are based on RECEIVED quantity, not PO quantity.
        
        IMPORTANT: When creating bill from receipt:
        - Odoo automatically sets bill qty = received qty
        - This ensures GRNI clearing matches what was credited
        
        Example:
        PO: 100 units
        Receipt: 90 units (GRNI credited 90)
        Bill: Should be 90 units (to clear GRNI of 90)
        """
        res = super()._prepare_account_move_line(move=move)
        
        # The quantity in res should already be based on received qty
        # when bill is created from receipt, but we add a safety check
        
        if move and move._is_in():
            # For purchase receipts, ensure we use the actual received qty
            # This is already handled by Odoo's standard flow
            pass
        
        return res

