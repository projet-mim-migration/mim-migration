# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp



class split_in_production_lot(osv.osv_memory):
    _name = "stock.move.split"
    _description = "Split in Serial Numbers"

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(split_in_production_lot, self).default_get(cr, uid, fields, context=context)
        if context.get('active_id'):
            move = self.pool.get('stock.move').browse(cr, uid, context['active_id'], context=context)
            if 'product_id' in fields:
                res.update({'product_id': move.product_id.id})
            if 'product_uom' in fields:
                res.update({'product_uom': move.product_uom.id})
            if 'qty' in fields:
                res.update({'qty': move.product_qty})
            if 'use_exist' in fields:
                res.update({'use_exist': (move.picking_id and move.picking_type_id == 2 and True) or False})
            if 'location_id' in fields:
                res.update({'location_id': move.location_id.id})
        return res

    _columns = {
        'qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'product_id': fields.many2one('product.product', 'Product', required=True, select=True),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure'),
        'line_ids': fields.one2many('stock.move.split.lines', 'wizard_id', 'Serial Numbers'),
        'line_exist_ids': fields.one2many('stock.move.split.lines', 'wizard_exist_id', 'Serial Numbers'),
        'use_exist' : fields.boolean('Existing Serial Numbers',
            help="Check this option to select existing serial numbers in the list below, otherwise you should enter new ones line by line."),
        'location_id': fields.many2one('stock.location', 'Source Location')
     }

    def split_lot(self, cr, uid, ids, context=None):
        """ To split a lot"""
        if context is None:
            context = {}
        new_move = self.split(cr, uid, ids, context.get('active_ids'), context=context)
        return {'type': 'ir.actions.act_window_close'}
    
    #v7
    def split(self, cr, uid, ids, move_ids, context=None):
        """ To split stock moves into serial numbers

        :param move_ids: the ID or list of IDs of stock move we want to split
        """
        if context is None:
            context = {}
        assert context.get('active_model') == 'stock.move',\
             'Incorrect use of the stock move split wizard'
        uom_obj = self.pool.get('product.uom')
        move_obj = self.pool.get('stock.move')
        prod_obj = self.pool.get('mrp.production')
        new_move = []
        for data in self.browse(cr, uid, ids, context=context):
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                move_qty = move.product_qty
                quantity_rest = move.product_qty
                uos_qty_rest = move.product_uos_qty
                new_move = []
                lines = [l for l in data.line_ids if l]
                if not lines:
                    raise osv.except_osv('Erreur',u"Impossible de diviser le mouvement car aucune ligne n'a été ajoutée.")
                total_move_qty = 0.0
                for line in lines:
                    quantity = line.quantity
                    total_move_qty += quantity
                    if total_move_qty > move_qty:
                        raise osv.except_osv('Processing Error!', 'Serial number quantity %d of %s is larger than available quantity (%d)!' \
                                % (total_move_qty, move.product_id.name, move_qty))
                    if quantity <= 0 or move_qty == 0:
                        continue
                    
                    quantity_rest -= quantity
                    uom_qty = uom_obj._compute_qty_obj(cr, uid, move.product_id.uom_id, quantity, move.product_uom, rounding_method='HALF-UP', context=context)
                    uos_qty = quantity / move_qty * move.product_uos_qty
                    
                    uos_qty_rest = quantity_rest / move_qty * move.product_uos_qty
                    if quantity_rest < 0:
                        raise osv.except_osv('Processing Error!', 'Unable to assign all lots to this move!')
                    
                    default_val = {
                        'product_uom_qty': uom_qty,
                        'product_uos_qty': uos_qty,
                        'procure_method': 'make_to_stock',
                        
                        'split_from': move.id,
                        'procurement_id': move.procurement_id.id,
                        'move_dest_id': move.move_dest_id.id,
                        'origin_returned_move_id': move.origin_returned_move_id.id,
                        'state': 'draft',
                        }
                    if quantity_rest > 0:
                        current_move = move_obj.copy(cr, uid, move.id, default_val, context=context)
                        new_move.append(current_move)
                        #creation ordre de fabrication
                        if move.id_mo:
                            prod_id = prod_obj.copy(cr, uid, move.id_mo, {
                                                                          'product_qty': uom_qty, 
                                                                          'move_prod_id': current_move,
                                                                          'origin': move.origin,
                                                                          }, context=context)
                            move_obj.write(cr, uid, [current_move], {'id_mo':prod_id})

                    update_val = {}
                    if quantity_rest > 0:
                        update_val['product_uom_qty'] = quantity_rest
                        update_val['product_uos_qty'] = uos_qty_rest
                        update_val['state'] = move.state
                        move_obj.write(cr, uid, [move.id], update_val)
                        #mise a jour ordre de fabrication lie
                        if move.id_mo:
                            prod_obj.write(cr, uid, [move.id_mo], {'product_qty':quantity_rest})
                    
                move_obj.action_confirm(cr, uid, new_move, context=context)
        return new_move
        
split_in_production_lot()

class stock_move_split_lines_exist(osv.osv_memory):
    _name = "stock.move.split.lines"
    _description = "Stock move Split lines"
    _columns = {
        'name': fields.char('Serial Number', size=64),
        'quantity': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'wizard_id': fields.many2one('stock.move.split', 'Parent Wizard'),
        'wizard_exist_id': fields.many2one('stock.move.split', 'Parent Wizard (for existing lines)'),
        'prodlot_id': fields.many2one('stock.production.lot', 'Serial Number'),
    }
    _defaults = {
        'quantity': 1.0,
    }

    def onchange_lot_id(self, cr, uid, ids, prodlot_id=False, product_qty=False,
                        loc_id=False, product_id=False, uom_id=False,context=None):
        return self.pool.get('stock.move').onchange_lot_id(cr, uid, [], prodlot_id, product_qty,
                        loc_id, product_id, uom_id, context)


class stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    #Redefinition pour prendre en compte les etats : contre_mesure, fiche_debit 
    def _state_get2(self, cr, uid, ids, field_name, arg, context=None):
        '''The state of a picking depends on the state of its related stock.move
            draft: the picking has no line or any one of the lines is draft
            done, draft, cancel: all lines are done / draft / cancel
            confirmed, waiting, assigned, partially_available depends on move_type (all at once or partial)
        '''
        res = {}
        for pick in self.browse(cr, uid, ids, context=context):
            if (not pick.move_lines) or any([x.state == 'draft' for x in pick.move_lines]):
                res[pick.id] = 'draft'
                continue
            if all([x.state == 'cancel' for x in pick.move_lines]):
                res[pick.id] = 'cancel'
                continue
            if all([x.state in ('cancel', 'done') for x in pick.move_lines]):
                res[pick.id] = 'done'
                continue
            #Prise en compte des etats contre_mesure et flowsheeting
            if all([x.state in ('contre_mesure','flowsheeting') for x in pick.move_lines]):
                res[pick.id] = 'confirmed'
                continue
            ########################################################
            order = {'confirmed': 0, 'waiting': 1, 'assigned': 2}
            order_inv = {0: 'confirmed', 1: 'waiting', 2: 'assigned'}
            
            #Ignorer les etats contre_mesure et flowsheeting
            lst = [order[x.state] for x in pick.move_lines if x.state not in ('cancel', 'done','contre_mesure','flowsheeting')]
            if lst==[]:
                continue
            ################################################
            if pick.move_type == 'one':
                res[pick.id] = order_inv[min(lst)]
            else:
                #we are in the case of partial delivery, so if all move are assigned, picking
                #should be assign too, else if one of the move is assigned, or partially available, picking should be
                #in partially available state, otherwise, picking is in waiting or confirmed state
                res[pick.id] = order_inv[max(lst)]
                if not all(x == 2 for x in lst) or any(x.state in ('contre_mesure','flowsheeting') for x in pick.move_lines) :
                    if any(x == 2 for x in lst):
                        res[pick.id] = 'partially_available'
                    else:
                        #if all moves aren't assigned, check if we have one product partially available
                        for move in pick.move_lines:
                            if move.partially_available:
                                res[pick.id] = 'partially_available'
                                break
        return res
    
    def _get_pickings(self, cr, uid, ids, context=None):
        res = set()
        for move in self.browse(cr, uid, ids, context=context):
            if move.picking_id:
                res.add(move.picking_id.id)
        return list(res)
    _columns = {
    'state': fields.function(_state_get2, type="selection", copy=False,
            store={
                'stock.picking': (lambda self, cr, uid, ids, ctx: ids, ['move_type'], 20),
                'stock.move': (_get_pickings, ['state', 'picking_id', 'partially_available'], 20)},
            selection=[
                ('draft', 'Draft'),
                ('cancel', 'Cancelled'),
                ('waiting', 'Waiting Another Operation'),
                ('confirmed', 'Waiting Availability'),
                ('partially_available', 'Partially Available'),
                ('assigned', 'Ready to Transfer'),
                ('done', 'Transferred'),
                ], string='Status', readonly=True, select=True, track_visibility='onchange',
            help="""
                * Draft: not confirmed yet and will not be scheduled until confirmed\n
                * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n
                * Waiting Availability: still waiting for the availability of products\n
                * Partially Available: some products are available and reserved\n
                * Ready to Transfer: products reserved, simply waiting for confirmation.\n
                * Transferred: has been processed, can't be modified or cancelled anymore\n
                * Cancelled: has been cancelled, can't be confirmed anymore"""
        ),
                }
    
    
stock_picking()

class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    #===========================================================================
    # def force_assign(self, cr, uid, ids, context=None):
    #     self.modifier_inventaire(cr, uid, ids, context=context)
    #     return super(stock_move, self).force_assign(cr, uid, ids, context=context)
    #===========================================================================
    
    def modifier_inventaire(self, cr, uid, ids, context=None):
        inventory_obj = self.pool.get('stock.inventory')
        inventory_line_obj = self.pool.get('stock.inventory.line')
        product_obj = self.pool.get('product.product')
        
        if context is None:
            context = {}
        
        move_data = self.browse(cr, uid, ids, context=context)[0]
        inventory_id = inventory_obj.create(cr, uid, {
                                                        'name': 'INV ' + move_data.product_id.name,
                                                        'filter': 'partial',
                                                        'location_id': move_data.location_id.id,
                                                        'state': 'draft',
                                                        }, context=context)
          
        prod_data = product_obj.browse(cr, uid, [move_data.product_id.id], context)[0]
        if prod_data.qty_available <= 0.0:
            qty_available = move_data.product_uom_qty
        else: 
            qty_available = move_data.product_uom_qty + prod_data.qty_available
        line_data = {
                    'inventory_id': inventory_id,
                    'product_qty': qty_available,
                    'location_id': move_data.location_id.id,
                    'product_id': move_data.product_id.id,
                    'product_uom_id': move_data.product_id.product_tmpl_id.uom_id.id,
                }           
        inventory_line_obj.create(cr , uid, line_data, context=context)
        inventory_obj.action_done(cr, uid, [inventory_id], context=context)
        inventory_obj.unlink(cr, uid, [inventory_id], context=context)
        
        return True