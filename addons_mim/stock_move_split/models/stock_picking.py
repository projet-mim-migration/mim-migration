# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _state_get2(self):
        res = {}
        for pick in self:
            if (not pick.move) or any([x.state == 'draft' for x in pick.move_lines]):
                res[pick.id] = 'draft'
                continue

            if all([x.state == 'cancel' for x in pick.move_lines]):
                res[pick.id] = 'cancel'
                continue

            if all([x.state in ('cancel', 'done') for x in pick.move_lines]):
                res[pick.id] = 'done'
                continue

            if all([x.state in ('contre_mesure', 'flowsheeting') for x in pick.move_lines]):
                res[pick.id] = 'confirmed'
                continue
            order = {'confirmed': 0, 'waiting': 1, 'assigned': 2}
            order_inv = {0: 'confirmed', 1: 'waiting', 2: 'assigned'}

            lst = [order[x.state] for x in pick.move_lines if
                   x.state not in ('cancel', 'done', 'contre_mesure', 'flowsheeting')]

            if not lst:
                continue

            if pick.move_type == 'one':
                res[pick.id] = order_inv[min(lst)]
            else:
                # we are in the case of partial delivery, so if all move are assigned, picking
                # should be assign too, else if one of the move is assigned, or partially available, picking should be
                # in partially available state, otherwise, picking is in waiting or confirmed state
                res[pick.id] = order_inv[max(lst)]
                if not all(x == 2 for x in lst) or any(
                        x.state in ('contre_mesure', 'flowsheeting') for x in pick.move_lines):
                    if any(x == 2 for x in lst):
                        res[pick.id] = 'partially_available'
                    else:
                        # if all moves aren't assigned, check if we have one product partially available
                        for move in pick.move_lines:
                            if move.partially_available:
                                res[pick.id] = 'partially_available'
                                break
        return res

    @api.multi
    def _get_picking(self):
        res = set()
        for move in self:
            if move.picking_id:
                res.add(move.pickin_id.id)
        return list(res)

    state = fields.Selection(selection=lambda self: self._state_get2(),
                             string='Status',
                             default=[
                                 ('draft', 'Draft'),
                                 ('cancel', 'Cancelled'),
                                 ('waiting', 'Waiting Another Operation'),
                                 ('confirmed', 'Waiting Availability'),
                                 ('partially_available', 'Partially Available'),
                                 ('assigned', 'Ready to Transfer'),
                                 ('done', 'Transferred'),
                             ])
