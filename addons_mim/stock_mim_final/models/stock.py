# -*- coding: utf-8 -*-

from odoo import models, fields, api 


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    @api.one
    #@api.depends('pick.move_lines', 'x.state', 'move.partially_available')
    def _state_get_new(self, field_name, arg):
        '''The state of a picking depends on the state of its related stock.move
            draft: the picking has no line or any one of the lines is draft
            done, draft, cancel: all lines are done / draft / cancel
            confirmed, waiting, assigned, partially_available depends on move_type (all at once or partial)
        '''
        res = {}
        for pick in self.browse():
            if (not pick.move_lines) or any([x.state == 'draft' for x in pick.move_lines]):
                res[pick.id] = 'draft'
                continue
            if all([x.state == 'cancel' for x in pick.move_lines]):
                res[pick.id] = 'cancel'
                continue
            if all([x.state in ('cancel', 'done') for x in pick.move_lines]):
                res[pick.id] = 'done'
                continue

            order = {'confirmed': 0, 'waiting': 1, 'assigned': 2}
            order_inv = {0: 'confirmed', 1: 'waiting', 2: 'assigned'}

            # Prise en considération des etats contre_mesure et fiche de débit
            b1 = True
            for x in pick.move_lines:
                if x.state in ('flowsheeting', 'contre_mesure'):
                    b0 = False
                else:
                    b0 = True
                b1 = b1 and b0

            if not b1:
                res[pick.id] = pick.state
            else:
                ###############################

                lst = [order[x.state] for x in pick.move_lines if x.state not in ('cancel', 'done')]
                if pick.move_type == 'one':
                    res[pick.id] = order_inv[min(lst)]
                else:
                    # we are in the case of partial delivery, so if all move are assigned, picking
                    # should be assign too, else if one of the move is assigned, or partially available, picking should be
                    # in partially available state, otherwise, picking is in waiting or confirmed state
                    res[pick.id] = order_inv[max(lst)]
                    if not all(x == 2 for x in lst):
                        if any(x == 2 for x in lst):
                            res[pick.id] = 'partially_available'
                        else:
                            # if all moves aren't assigned, check if we have one product partially available
                            for move in pick.move_lines:
                                if move.partially_available:
                                    res[pick.id] = 'partially_available'
                                    break
        return res

    @api.one
    def _get_pickings(self):
        res = set()
        for move in self.browse():
            if move.picking_id:
                res.add(move.picking_id.id)
        return list(res)

    
    state = fields.Selection(compute=_state_get_new, copy=False,
                                 selection=[
                                     ('draft', 'Draft'),
                                     ('cancel', 'Cancelled'),
                                     ('waiting', 'Waiting Another Operation'),
                                     ('confirmed', 'Waiting Availability'),
                                     ('partially_available', 'Partially Available'),
                                     ('assigned', 'Ready to Transfer'),
                                     ('done', 'Transferred'),
                                 ], string='Status', readonly=True, select=True,
                                 help="""
                * Draft: not confirmed yet and will not be scheduled until confirmed\n
                * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n
                * Waiting Availability: still waiting for the availability of products\n
                * Partially Available: some products are available and reserved\n
                * Ready to Transfer: products reserved, simply waiting for confirmation.\n
                * Transferred: has been processed, can't be modified or cancelled anymore\n
                * Cancelled: has been cancelled, can't be confirmed anymore"""
                                 )
