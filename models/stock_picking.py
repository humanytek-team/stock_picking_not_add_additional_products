# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, models
from openerp.exceptions import ValidationError
from openerp.tools.translate import _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_new_transfer(self):

        if not self.user_has_groups('stock.group_stock_manager'):
            for pick in self:

                if pick.picking_type_code == 'incoming' and \
                        pick.purchase_id:

                    for pack_operation in pick.pack_operation_product_ids:

                        if pack_operation.product_id.id not in \
                            pick.purchase_id.mapped(
                                'order_line.product_id.id'):

                            raise ValidationError(
                                _('You cannot add additional products to those in the source document.')
                                )

                elif pick.picking_type_code == 'outgoing' and pick.sale_id:

                    for pack_operation in pick.pack_operation_product_ids:

                        if pack_operation.product_id.id not in \
                            pick.sale_id.mapped(
                                'order_line.product_id.id'):

                            raise ValidationError(
                                _('You cannot add additional products to those in the source document.')
                                )

        return super(StockPicking, self).do_new_transfer()
