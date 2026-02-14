{
    'name': 'AK Stock Input/Output Accounts',
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
    'depends': ['stock_account'],
    'data': [
        'views/product_category_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
