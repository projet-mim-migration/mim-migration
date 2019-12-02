# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.tools.translate import _

class stock_move(models.Model):

    _inherit = 'stock.move'
    
    def flow_sheet(self):
      if self.state == 'contre_mesure':
        self.state = 'flowsheeting'
      else:
        pass

    def flow_sheet_cancel(self):
      if self.state == 'flowsheeting':
        self.state = 'contre_mesure'
      else:
        pass


    state = fields.Selection([('draft', 'New'),
                                   ('cancel', 'Cancelled'),
                                   ('waiting', 'Waiting Another Move'),
                                   ('confirmed', 'Waiting Availability'),
                                   ('flowsheeting',u'Fiche de Débit'),
                                   ('assigned', 'Available'),
                                   ('done', 'Done'),
                                   ], 'Status', readonly=True, select=True,
                 help= "* New: When the stock move is created and not yet confirmed.\n"\
                       "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"\
                       "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to me manufactured...\n"\
               "* Fiche de Debit: the state is \'Fiche de Debit\'.\n"
                       "* Available: When products are reserved, it is set to \'Available\'l.\n"\
                       "* Done: When the shipment is processed, the state is \'Done\'.")


    