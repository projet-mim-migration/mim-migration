# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import odoo.addons.decimal_precision as dp


class split_in_production_lot(models.TransientModel):
    _name = 'stock.move.split'
    _description = 'Split in serial numbers'

    qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    product_id = fields.Many2one('product.product', 'Product', required=True, index=True)
    product_uom = fields.Many2one('uom.uom', string='Unit of measures')
    line_ids = fields.One2many('stock.move.split.lines', 'wizard_id', string='Serial Numbers')
    line_exist_ids = fields.One2many('stock.move.split.lines', 'wizard_exist_id', 'Serial Numbers')
    use_exist = fields.Boolean('Existing Serial Number', help="Check this option to select existing serial numbers in "
                                                              "the list below, otherwise you should enter new ones "
                                                              "line by line.")
    location_id = fields.Many2one('stock.location', string='Source Location')

    @api.model
    def default_get(self, fields_list):
        res = super(split_in_production_lot, self).default_get(fields_list)
        move = self.env['stock.move'].browse(self.env.context.get('active_id'))

        res.update({
            'product_id': move.product_id.id,
            'product_uom': move.product_uom.id,
            'qty': move.product_qty,
            'use_exist': ((move.picking_id and move.picking_type_id == 2 and True) or False),
            'location_id': move.location_id.id
        })

        return res

    @api.multi
    def split_lot(self):
        self.split(self.env.context.get('active_ids'))
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def split(self, move_ids):
        uom_obj = self.env['uom.uom']
        move_obj = self.env['stock.move']
        prod_obj = self.env['mrp.production']
        new_move = []

        for data in self:

            # Pour chaque mouvement de stock
            for move in move_obj.browse(move_ids):
                move_qty = move.product_qty
                quantity_rest = move.product_qty
                new_move = []

                # Les lignes
                lines = [l for l in data.line_ids if l]
                if not lines:
                    raise exceptions.ValidationError(
                        'Erreur, Impossible de diviser le mouvement car aucune ligne n\'a été ajoutée.')

                total_move_qty = 0.0

                # Pour chaque ligne
                for line in lines:
                    quantity = line.quantity
                    total_move_qty += quantity
                    if total_move_qty > move_qty:
                        continue

                    quantity_rest -= quantity
                    uom_qty = uom_obj.search([('id', '=', move.product_id.uom_id.id)])._compute_quantity(quantity, self.product_uom)
                    # uos_qty = quantity / move_qty * move.product_uos_qty

                    # uos_qty_rest = quantity_rest / move_qty * move.product_uos_qty
                    if quantity_rest < 0:
                        raise exceptions.ValidationError('Processing error, Unable to assign all lots to this move!')

                        # 'product_uos_qty': uos_qty,

                    default_val = {
                        'product_uom_qty': uom_qty,
                        # 'procure_method': 'make_to_stock',

                        'split_from': move.id,
                        # 'procurement_id': move.procurement_id.id,
                        'move_dest_ids': move.move_dest_ids.id,
                        'origin_returned_move_id': move.origin_returned_move_id.id,
                        'state': 'draft',
                    }

                    if quantity_rest > 0:
                        current_move = move_obj.search([('id', '=', move.id)]).copy(default_val)
                        new_move.append(current_move)

                        if move.id_mo:
                            prod_id = prod_obj.browse(move.id_mo).copy({'product_qty': uom_qty,
                                                                        'move_prod_id': current_move,
                                                                        'origin': move.origin,
                                                                        })
                            move_obj.browse(current_move).write({'id_mo', prod_id})

                    update_val = {}
                    if quantity_rest > 0:
                        update_val['product_uom_qty'] = quantity_rest
                        # update_val['product_uos_qty'] = uos_qty_rest
                        update_val['state'] = move.state
                        move_obj.browse(move.id).write(update_val)

                        if move.id_mo:
                            prod_obj.browse(move.id_mo).write({'product_qty': quantity_rest})

                # move_obj.action_confirm()
        return new_move
