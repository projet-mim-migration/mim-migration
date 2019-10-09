# Written by Lido on  Licence GPL #
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields

class stock_move(osv.Model):

    _inherit = 'stock.move'
    _columns = {
    'state': fields.selection([('draft', 'New'),
                                   ('cancel', 'Cancelled'),
                                   ('waiting', 'Waiting Another Move'),
                                   ('confirmed', 'Waiting Availability'),
                                   ('contre_mesure', 'Contre mesure'),
                                   ('flowsheeting',u'Fiche de Débit'),
                                   ('assigned', 'Available'),
                                   ('done', 'Done'),
                                   ], 'Status', readonly=True, select=True,
                 help= "* New: When the stock move is created and not yet confirmed.\n"\
                       "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"\
                       "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to me manufactured...\n"\
               "* Fiche de Debit: the state is \'Fiche de Debit\'.\n"
                       "* Available: When products are reserved, it is set to \'Available\'l.\n"\
                       "* Done: When the shipment is processed, the state is \'Done\'."),
    }
