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

{
    'name': 'Restore Stock Input/Output Accounts in v19',
    'version': '19.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Restore Stock Input and Output Account fields to Product Categories',
    'description': """
        This module restores the Stock Input Account and Stock Output Account fields
        to Product Categories in Odoo 19, similar to previous versions.
        
        Features:
        - Adds Stock Input Account field to product categories
        - Adds Stock Output Account field to product categories
        - Automatically applies these accounts during stock moves when configured
        - Compatible with both Perpetual and Periodic valuation methods
        
        Accounting Behavior:
        - Purchase: Journal entries created on product receipt with Stock Input Account
        - Sales: Journal entries created on delivery with Stock Output Account
    """,
    'author': 'Alkia IT Services',
    'website': 'https://www.alkia.net',
    'depends': ['stock_account', 'purchase'],
    'data': [
        'views/product_category_views.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
