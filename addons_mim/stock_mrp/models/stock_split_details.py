# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo  import netsvc


class stock_split_details(models.TransientModel):
    _name = 'stock.split_details'
    _description = 'Split picking wizard'
    
    def _get_picking_id(self):
        if self.env.context is None: self.env.context = {}
        return self.env.context.get('picking_id', False)

    @api.model
    def default_get(self, fields):
        # We override the default_get to make stock moves created after the picking was confirmed
        # directly as available. This allows to create extra move lines in
        # the fp view.
        res = super(stock_split_details, self).default_get(fields)
        if self.env.context.get('default_picking_id'):
            move = self.env['stock.picking'].browse(self.env.context['default_picking_id'])
            if move.state == 'done':
                res['state'] = 'done'
                res['product_uom_qty'] = 0.0
                res['additional'] = True
            elif move.state not in ['draft', 'confirmed']:
                res['state'] = 'assigned'
                res['product_uom_qty'] = 0.0
                res['additional'] = True
        return res

    picking_id = fields.Many2one('stock.picking', 'Picking', default=_get_picking_id)
    item_ids = fields.One2many('stock.split_details_items', 'transfer_id', 'Items', domain=[('product_id', '!=', False)])
    
    @api.one
    def do_split(self):
        picking_obj = self.env['stock.picking']
        move_obj = self.env["stock.move"]
        prod_obj = self.env['mrp.production']
        wf_service = netsvc.LocalService("workflow")
        split = self.browse()[0]
        backorder_move_ids = []
        for item in split.item_ids:
            if item.move_id.product_uom_qty < item.quantity:
                raise self.env.osv.except_osv(('Erreur!'),
                                     ("La quantité entrée %s %s est supérieur à celle du mouvement de stock parent.")
                                     % (item.quantity, item.product_id.name))
            if item.move_id.product_uom_qty == item.quantity:
                backorder_move_ids.append(item.move_id.id)
            if item.move_id.product_uom_qty > item.quantity:
                new_move_id = move_obj.copy(item.move_id.id, {'product_uom_qty': item.quantity})
                move_obj.action_confirm([new_move_id])
                # creation ordre de fabrication
                if item.move_id.id_mo:
                    prod_id = prod_obj.copy(item.move_id.id_mo, {
                        'product_qty': item.quantity,
                        'move_prod_id': new_move_id,
                        'origin': item.move_id.origin,
                    }, context=self.env.context)
                    move_obj.write([new_move_id], {'id_mo': prod_id})

                state_origin = item.move_id.state
                # workflow
                if state_origin == 'contre_mesure':
                    wf_service.trg_validate( 'stock.move', new_move_id, 'contre_mesure')
                if state_origin == 'flowsheeting':
                    wf_service.trg_validate('stock.move', new_move_id, 'contre_mesure')
                    wf_service.trg_validate('stock.move', new_move_id, 'flow_sheet')
                if state_origin == 'assigned':
                    wf_service.trg_validate('stock.move', new_move_id, 'contre_mesure')
                    wf_service.trg_validate('stock.move', new_move_id, 'flow_sheet')
                    wf_service.trg_validate('stock.move', new_move_id, 'force_assign')

                backorder_move_ids.append(new_move_id)
                new_qty = item.move_id.product_uom_qty - item.quantity
                move_obj.write([item.move_id.id], {'product_uom_qty': new_qty})

                # mise a jour ordre de fabrication lie
                if item.move_id.id_mo:
                    prod_obj.write([item.move_id.id_mo], {'product_qty': new_qty})

        if backorder_move_ids:
            backorder_id = picking_obj.copy(split.picking_id.id, {
                'name': '/',
                'move_lines': [],
                'pack_operation_ids': [],
                'backorder_id': split.picking_id.id,
            })
            backorder = picking_obj.browse(backorder_id)
            picking_obj.message_post(split.picking_id.id,
                                     body=("Reliquat <em>%s</em> <b>créé</b>.") % (backorder.name))
            move_obj.write(self.cr, self.env.uid, backorder_move_ids, {'picking_id': backorder_id})

            picking_obj.action_confirm([backorder_id])
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
    quantity = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), default=1.0)
    sourceloc_id = fields.Many2one('stock.location', 'Source Location', required=True)
    destinationloc_id = fields.Many2one('stock.location', 'Destination Location', required=True)
    move_id = fields.Many2one('stock.move', 'Mouvement de stock')
    name = fields.Char('Description')

    @api.multi
    def split(self):
        for det in self:
            if det.quantity > 1:
                det.quantity = (det.quantity - 1)
                new_id = det.copy(context=self.env.context)
                new_id.quantity = 1
        if self and self[0]:
            return self[0].transfer_id.wizard_view()