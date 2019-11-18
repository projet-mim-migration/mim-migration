# -*- coding: utf-8 -*-

from odoo import netsvc
import time

from odoo import fields, models, exceptions, api, _

class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'
    
    #Modifification de la fonction retour d'article pour le cas particulier d'un retour via un orde de fabrication
    @api.multi
    def _create_returns(self):
        self.ensure_one()

        context = dict(self.env.context or {})
        record_id = context and context.get('active_id', False) or False
        move_obj = self.env['stock.move']
        pick_obj = self.env['stock.picking']
        data_obj = self.env['stock.return.picking.line']
        pick = pick_obj.browse(record_id)
        data = self.read(self.id)
        returned_lines = 0

        # Cancel assignment of existing chained assigned moves
        moves_to_unreserve = []
        for move in pick.move_lines:
            to_check_moves = [move.move_dest_id] if move.move_dest_id.id else []
            while to_check_moves:
                current_move = to_check_moves.pop()
                if current_move.state not in ('done', 'cancel') and current_move.reserved_quant_ids:
                    moves_to_unreserve.append(current_move.id)
                split_move_ids = move_obj.search([('split_from', '=', current_move.id)])
                if split_move_ids:
                    to_check_moves += move_obj.browse(split_move_ids)

        if moves_to_unreserve:
            move_obj.do_unreserve(moves_to_unreserve)
            #break the link between moves in order to be able to fix them later if needed
            move_obj.browse(moves_to_unreserve).write({
                'move_orig_ids': False
            })

        #Create new picking for returned products
        pick_type_id = pick.picking_type_id.return_picking_type_id and pick.picking_type_id.return_picking_type_id.id or pick.picking_type_id.id
        new_picking = pick_obj.browse(pick.id).copy({
            'move_lines': [],
            'picking_type_id': pick_type_id,
            'state': 'draft',
            'origin': pick.name,
        })

        for data_get in data_obj.browse(data['product_return_moves']):
            move = data_get.move_id
            if not move:
                raise exceptions.UserError(_("You have manually created product lines, please delete them to proceed"))
            new_qty = data_get.quantity
            if new_qty:
                # The return of a return should be linked with the original's destination move if it was not cancelled
                if move.origin_returned_move_id.move_dest_id.id and move.origin_returned_move_id.move_dest_id.state != 'cancel':
                    move_dest_id = move.origin_returned_move_id.move_dest_id.id
                else:
                    move_dest_id = False
                
                
                # Modification
                new_location = move.location_dest_id.id
                if ':MO' in pick.origin and pick.picking_type_id.id==3 and 'return' not in pick.name and 'retour' not in pick.name:
                    self._cr.execute("SELECT s.id FROM stock_location s WHERE s.name ='Production'")
                    res = self._cr.dictfetchone()
                    new_location = res.get('id', new_location)
                ##################################
                
                returned_lines += 1
                move_obj.browse(move.id).copy({
                    'product_id' : data_get.product_id.id,
                    'product_uom_qty' : new_qty,
                    'product_uos_qty' : new_qty * move.product_uos_qty / move.product_uom_qty,
                    'picking_id' : new_picking,
                    'state' : 'draft',
                    'location_id' : new_location,
                    'location_dest_id' : move.location_id.id,
                    'picking_type_id' : pick_type_id,
                    'warehouse_id' : pick.picking_type_id.warehouse_id.id,
                    'origin_returned_move_id' : move.id,
                    'procure_method' : 'make_to_stock',
                    'restrict_lot_id' : data_get.lot_id.id,
                    'move_dest_id' : move_dest_id,
                })

        if not returned_lines:
            raise exceptions.UserError(_("Please specify at least one non-zero quantity."))

        pick_obj.action_confirm([new_picking])
        pick_obj.action_assign([new_picking])
        return new_picking, pick_type_id
