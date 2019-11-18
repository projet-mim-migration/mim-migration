# -*- coding: utf-8 -*-

from odoo  import models, fields, api


class stock_transfer_details(models.Model):
    _inherit = 'stock.picking'

    def default_get(self, fields=None):
        if fields is None: fields = {}
        res = super(stock_transfer_details, self).default_get(fields)
        picking_ids = self._context.get('active_ids', [])
        active_model = self._context.get('active_model')

        if not picking_ids or len(picking_ids) != 1:
            # Partial Picking Processing may only be done for one picking at a time
            return res
        assert active_model in ('stock.picking'), 'Bad context propagation'
        picking_id, = picking_ids
        picking = self.env['stock.picking'].browse(picking_id)
        items = []
        packs = []
        # enlever car il faut toujours effectuer un do_prepare_partial() à chaque livraison (partielle ou totale)
        # if not picking.pack_operation_ids:
        picking.do_prepare_partial()
        for op in picking.pack_operation_ids:
            item = {
                'packop_id': op.id,
                'product_id': op.product_id.id,
                'product_uom_id': op.product_uom_id.id,
                'quantity': op.product_qty,
                'package_id': op.package_id.id,
                'lot_id': op.lot_id.id,
                'sourceloc_id': op.location_id.id,
                'destinationloc_id': op.location_dest_id.id,
                'result_package_id': op.result_package_id.id,
                'date': op.date,
                'owner_id': op.owner_id.id,
            }
            if op.product_id:
                items.append(item)
            elif op.package_id:
                packs.append(item)
        res.update(item_ids=items)
        res.update(packop_ids=packs)
        return res