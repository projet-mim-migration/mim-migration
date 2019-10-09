# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.osv import osv
import openerp.addons.decimal_precision as dp
from openerp import netsvc

class stock_split_details(models.TransientModel):
    _name = 'stock.split_details'
    _description = 'Split picking wizard'
    
    def _get_picking_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('picking_id', False)
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        res = super(stock_split_details, self).default_get(cr, uid, fields, context=context)
        picking_ids = context.get('active_ids', [])
        
        if not picking_ids or len(picking_ids) != 1:
            return res
        picking_id, = picking_ids
        picking = self.pool.get('stock.picking').browse(cr, uid, picking_id, context=context)
        items = []
        if not picking.move_lines:
            raise osv.except_osv(('Erreur!'),(u"Le bon de livraison ne contient aucun mouvement de stock"))
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

    picking_id = fields.Many2one('stock.picking', 'Picking', default=_get_picking_id)
    item_ids = fields.One2many('stock.split_details_items', 'transfer_id', 'Items', domain=[('product_id', '!=', False)])
    
    def do_split(self, cr, uid, ids, context=None):
        picking_obj = self.pool.get('stock.picking')
        move_obj = self.pool.get("stock.move")
        prod_obj = self.pool.get('mrp.production')
        wf_service = netsvc.LocalService("workflow")
        split = self.browse(cr, uid, ids, context=context)[0]
        backorder_move_ids = []
        for item in split.item_ids:
            if item.move_id.product_uom_qty<item.quantity:
                raise osv.except_osv(('Erreur!'),
                                     (u"La quantité entrée %s %s est supérieur à celle du mouvement de stock parent.")
                                      % (item.quantity, item.product_id.name))
            if item.move_id.product_uom_qty==item.quantity:
                backorder_move_ids.append(item.move_id.id)
            if item.move_id.product_uom_qty>item.quantity:
                new_move_id = move_obj.copy(cr, uid, item.move_id.id, {'product_uom_qty': item.quantity})
                move_obj.action_confirm(cr, uid, [new_move_id], context=context)
                #creation ordre de fabrication
                if item.move_id.id_mo:
                    prod_id = prod_obj.copy(cr, uid, item.move_id.id_mo, {
                                                                          'product_qty': item.quantity, 
                                                                          'move_prod_id': new_move_id, 
                                                                          'origin': item.move_id.origin,
                                                                          }, context=context)
                    move_obj.write(cr, uid, [new_move_id], {'id_mo':prod_id})
                    
                state_origin = item.move_id.state
                #workflow
                if state_origin=='contre_mesure':
                    wf_service.trg_validate(uid, 'stock.move', new_move_id, 'contre_mesure', cr)
                if state_origin=='flowsheeting':
                    wf_service.trg_validate(uid, 'stock.move', new_move_id, 'contre_mesure', cr)
                    wf_service.trg_validate(uid, 'stock.move', new_move_id, 'flow_sheet', cr)
                if state_origin=='assigned':
                    wf_service.trg_validate(uid, 'stock.move', new_move_id, 'contre_mesure', cr)
                    wf_service.trg_validate(uid, 'stock.move', new_move_id, 'flow_sheet', cr)
                    wf_service.trg_validate(uid, 'stock.move', new_move_id, 'force_assign', cr)
                    
                backorder_move_ids.append(new_move_id)
                new_qty = item.move_id.product_uom_qty-item.quantity
                move_obj.write(cr, uid, [item.move_id.id], {'product_uom_qty': new_qty}, context=context)
                
                #mise a jour ordre de fabrication lie
                if item.move_id.id_mo:
                    prod_obj.write(cr, uid, [item.move_id.id_mo], {'product_qty': new_qty})
                
        if backorder_move_ids:
            backorder_id = picking_obj.copy(cr, uid, split.picking_id.id, {
                'name': '/',
                'move_lines': [],
                'pack_operation_ids': [],
                'backorder_id': split.picking_id.id,
            })
            backorder = picking_obj.browse(cr, uid, backorder_id, context=context)
            picking_obj.message_post(cr, uid, split.picking_id.id, body=(u"Reliquat <em>%s</em> <b>créé</b>.") % (backorder.name), context=context)
            move_obj.write(cr, uid, backorder_move_ids, {'picking_id': backorder_id}, context=context)

            picking_obj.action_confirm(cr, uid, [backorder_id], context=context)
        return True
    
    @api.multi
    def wizard_view(self):
        view = self.env.ref('stock_mrp.view_stock_split_details')

        return {
            'name': u'Entrer les quantités à diviser',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.split_details',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.ids[0],
            'context': self.env.context,
        }
        
class stock_split_details_items(models.TransientModel):
    _name = 'stock.split_details_items'
    _description = 'Split picking wizard items'

    transfer_id = fields.Many2one('stock.split_details', 'Split')
    product_id = fields.Many2one('product.product', 'Product')
    product_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure')
    quantity = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), default = 1.0)
    sourceloc_id = fields.Many2one('stock.location', 'Source Location', required=True)
    destinationloc_id = fields.Many2one('stock.location', 'Destination Location', required=True)
    move_id = fields.Many2one('stock.move', 'Mouvement de stock')
    name = fields.Char('Description')
    
    @api.multi
    def split(self):
        for det in self:
            if det.quantity>1:
                det.quantity = (det.quantity-1)
                new_id = det.copy(context=self.env.context)
                new_id.quantity = 1
        if self and self[0]:
            return self[0].transfer_id.wizard_view()