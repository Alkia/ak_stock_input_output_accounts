################################################################################
# Module:        Stock Input/Output Accounts Module for Odoo 19                   
# Version:       119.0.2.16.0                      
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
 
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    # Stock Variation Account (reinstated for Odoo 19; standard field was removed)
    property_ak_stock_variation_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Stock Variation',
        company_dependent=True,
        help="Account for stock value variations (e.g. revaluation, adjustments).",
    )
    # Price Difference Account (e.g. for manual periodic valuation)
    property_ak_stock_price_difference_categ_id = fields.Many2one(
        comodel_name='account.account',
        string='Price Difference Account',
        company_dependent=True,
        help="Account used for price differences (e.g. PO vs Bill variance).",
    )
    # Stock Input Account (incoming stock moves)
    property_stock_account_input_categ_id = fields.Many2one(
        comodel_name='account.account',
        string='Stock Input Account',
        company_dependent=True,
        help="Counterpart journal items for all incoming stock moves will be posted in this account, "
             "unless there is a specific valuation account set on the source location. "
             "This is the default value for all products in this category. "
             "It can also directly be set on each product.",
    )
    # Stock Output Account (outgoing stock moves)
    property_stock_account_output_categ_id = fields.Many2one(
        comodel_name='account.account',
        string='Stock Output Account',
        company_dependent=True,
        help="When doing automated inventory valuation, counterpart journal items for all outgoing "
             "stock moves will be posted in this account, unless there is a specific valuation "
             "account set on the destination location. This is the default value for all products "
             "in this category. It can also directly be set on each product.",
    )
