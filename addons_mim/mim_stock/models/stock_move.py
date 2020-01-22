    # -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

import time
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    state = fields.Selection(
        [('draft', 'New'),
         ('cancel', 'Cancelled'),
         ('waiting', 'Waiting Another Move'),
         ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
         ('contre_mesure', 'Contre mesure'),
         ('flowsheeting', u'Fiche de Débit'),
         ('assigned', 'Available'),
         ('done', 'Done'),], 
        'Status', 
        readonly=True, 
        help="* New: When the stock move is created and not yet confirmed.\n" \
             "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n" \
             "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to me manufactured...\n" \
             "* Fiche de Debit: the state is \'Fiche de Debit\'.\n"
             "* Available: When products are reserved, it is set to \'Available\'l.\n" \
             "* Done: When the shipment is processed, the state is \'Done\'."
    )
    date_prevue = fields.Datetime(
        'Date prevue', 
        help="Date prevue", 
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    )
    min_date = fields.Datetime(
        'Date de contre-mesure', 
        help="Date de contre-mesure", 
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, 
        default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    )
    date = fields.Datetime(
        'Date de livraison', 
        help="Date de livraison", 
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, 
        default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    )
    name = fields.Text(
        'Description', 
        required=True, 
        select=True
    )


    # Manage the workflow
    def contre_mesure1(self):
        self.state = 'contre_mesure'

    def annuler_contre_mesure(self):
        if self.state == 'contre_mesure':
            self.state = 'confirmed'

    def flow_sheet(self):
        if self.state == 'contre_mesure':
            self.state = 'flowsheeting'

    def flow_sheet_cancel(self):
        if self.state == 'flowsheeting':
            self.state = 'contre_mesure'

    def force_assign(self):
        if self.state == 'flowsheeting':
            self.state = 'assigned'


    @api.multi
    def write(self, vals):
        context = self.env.context or {}
        res = super(StockMove, self).write(vals)
        
        #mise a jour ordre de fabrication
        if vals.get('largeur') or vals.get('hauteur') or vals.get('is_printable'):
            mo_vals = {
                       'largeur':self.largeur,
                       'hauteur': self.hauteur,
                       'is_printable': self.is_printable,
                       }
            self.env['mrp.production'].browse(self.id_mo).write(mo_vals)
        
        #mise a jour date de production
        pick_obj = self.env['stock.picking']
        date_now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        if vals.get('state'):
            for move in self:
                pick = pick_obj.browse(move.picking_id.id)
                if all(x.state == 'assigned' for x in pick.move_lines) and not pick.production_date:
                    pick_obj.browse(pick.id).write({'production_date': date_now})
                if all(x.state == 'done' for x in pick.move_lines) and not pick.delivery_date:
                    pick_obj.browse(pick.id).write({'delivery_date': date_now})
        return res

    # Make the product unavaillable
    def _action_assign(self):
        super(StockMove, self)._action_assign()
        
        for move in self:
            if move.picking_id.state == 'assigned' and not move.picking_id.mo_created:
                move.picking_id.do_unreserve()