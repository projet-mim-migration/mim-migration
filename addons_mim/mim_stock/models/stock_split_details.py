# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import odoo.addons.decimal_precision as dp


class StockSplitDetails(models.TransientModel):
    _name = 'stock.split_details'
    _description = 'Split picking wizard'
    
    def _get_picking_id(self):
        context = self.env.context or {}
        return context.get('picking_id', False)
    
    picking_id = fields.Many2one(
        'stock.picking', 
        'Picking', 
        default=_get_picking_id
    )
    item_ids = fields.One2many(
        'stock.split_details_items', 
        'transfer_id', 
        'Items', 
        domain=[('product_id', '!=', False)]
    )

    def default_get(self, fields):
        context = self.env.context or {}
        res = super(StockSplitDetails, self).default_get(fields)
        picking_ids = context.get('active_pick_ids', [])
        
        if not picking_ids or len(picking_ids) != 1:
            return res
        picking_id = picking_ids
        picking = self.env['stock.picking'].browse(picking_id)
        items = []
        if not picking.move_lines:
            raise exceptions.UserError(u"Le bon de livraison ne contient aucun mouvement de stock")
        for move in picking.move_lines:
            item = {
                'product_id': move.product_id.id,
                'product_uom_id': move.product_uom.id,
                'quantity': move.product_uom_qty,
                'sourceloc_id': move.location_id.id,
                'destinationloc_id': move.location_dest_id.id,
                'move_id': move.id,
                'name': move.name,
            }
            items.append(item)
        res.update(item_ids=items)
        return res

    
    @api.multi
    def do_split(self):
        self.ensure_one()

        picking_obj = self.env['stock.picking']
        move_obj = self.env["stock.move"]
        prod_obj = self.env['mrp.production']
        
        backorder_move_ids = []
        for item in self.item_ids:
            if item.move_id.product_uom_qty < item.quantity:
                raise exceptions.UserError((u"La quantité entrée %s %s est supérieur à celle du mouvement de stock parent.")
                                      % (item.quantity, item.product_id.name))
            if item.move_id.product_uom_qty == item.quantity:
                backorder_move_ids.append(item.move_id.id)
            if item.move_id.product_uom_qty > item.quantity:
                new_move_id = move_obj.browse(item.move_id.id).copy({'product_uom_qty': item.quantity})
                move_obj.action_confirm(new_move_id)
                #creation ordre de fabrication
                if item.move_id.id_mo:
                    prod_id = prod_obj.browse(item.move_id.id_mo).copy({'product_qty': item.quantity, 
                                                                        # 'move_prod_id': new_move_id, 
                                                                        'origin': item.move_id.origin,
                    })
                    move_obj.browse(new_move_id).write({'id_mo':prod_id})
                    
                state_origin = item.move_id.state

                new_move = move_obj.browse(new_move_id)
               
                #workflow
                if state_origin=='contre_mesure':
                    new_move.contre_mesure1()
                if state_origin=='flowsheeting':
                    new_move.contre_mesure1()
                    new_move.flow_sheet()
                if state_origin=='assigned':
                    new_move.contre_mesure1()
                    new_move.flow_sheet()
                    new_move.force_assign()
                    
              
                backorder_move_ids.append(new_move_id)
                new_qty = item.move_id.product_uom_qty - item.quantity
                move_obj.browse(item.move_id.id).write({'product_uom_qty': new_qty})
                
                #mise a jour ordre de fabrication lie
                if item.move_id.id_mo:
                    prod_obj.browse(item.move_id.id_mo).write({'product_qty': new_qty})
                
        if backorder_move_ids:
            backorder = picking_obj.browse(self.picking_id.id).copy({
                'name': '/',
                'move_lines': [],
                'pack_operation_ids': [],
                'backorder_id': self.picking_id.id,
            })
            
            picking_obj.browse(self.picking_id.id).message_post(body=(u"Reliquat <em>%s</em> <b>créé</b>.") % (backorder.name))
            move_obj.browse(backorder_move_ids).write({'picking_id': backorder.id})

            backorder.action_confirm()
            
        return True
    
    @api.multi
    def wizard_view(self):
        view = self.env.ref('mim_stock.view_stock_split_details')
        
        return {
            'name': u'Entrer les quantités à diviser',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.split_details',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            # Use of self.id.id because there are bug :/
            'res_id': self.id.id,
            'context': self.env.context,
        }
        
class StockSplitDetailsItems(models.TransientModel):
    _name = 'stock.split_details_items'
    _description = 'Split picking wizard items'

    transfer_id = fields.Many2one(
        'stock.split_details', 
        'Split'
    )
    product_id = fields.Many2one(
        'product.product', 
        'Product'
    )
    product_uom_id = fields.Many2one(
        'product.uom', 
        'Product Unit of Measure'
    )
    quantity = fields.Float(
        'Quantity', 
        digits=dp.get_precision('Product Unit of Measure'), 
        default = 1.0
    )
    sourceloc_id = fields.Many2one(
        'stock.location', 
        'Source Location', 
        required=True
    )
    destinationloc_id = fields.Many2one(
        'stock.location', 
        'Destination Location', 
        required=True
    )
    move_id = fields.Many2one(
        'stock.move', 
        'Mouvement de stock'
    )
    name = fields.Char(
        'Description'
    )
    
    @api.multi
    def split(self):
        for det in self:
            if det.quantity > 1:
                det.quantity = (det.quantity-1)
                new_id = det.copy(context=self.env.context)
                new_id.quantity = 1
        if self and self[0]:
            return self[0].transfer_id.wizard_view()