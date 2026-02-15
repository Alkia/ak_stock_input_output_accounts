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
