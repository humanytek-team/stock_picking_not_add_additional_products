# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, models
from openerp.exceptions import ValidationError
from openerp.tools.translate import _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def write(self, vals):
        if not self.user_has_groups('stock.group_stock_manager'):
            if self.picking_type_id.code in ['incoming', 'outgoing']:
                if 'pack_operation_product_ids' in vals.keys():
                    for line in vals['pack_operation_product_ids']:
                        if line[0] == 0 and not line[1] and \
                                isinstance(line[2], dict):

                            raise ValidationError(
                                _('You cannot add additional products to those in the source document.')
                                )

        return super(StockPicking, self).write(vals)
