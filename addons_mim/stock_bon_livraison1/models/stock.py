# -*- coding: utf-8 -*-
import time
from datetime import datetime

from odoo import models, fields, api


class stock_picking(models.Model):
    _inherit = "stock.picking"

    motivation = fields.Text('Motivation')
    date_changed = fields.Boolean('Date changée', default=False)


    # Evenement losrque la date de livraison est modifié
    @api.one
    def onchange_fields(self):
        if len(ids) > 0:
            return {'value': {'date_changed': True}}
        else:
            return {'value': {'date_changed': False}}

    @api.one
    def write(self, vals):
        # picking_data = self.browse(cr, uid, ids, context=context)[0]
        user_obj = self.env['res.users']
        # uids = user_obj.search(cr, uid, [('id','=',uid)], context=context)
        user = user_obj.browse()

        if 'date_changed' in vals:
            if vals['date_changed'] == True:
                if 'motivation' in vals:
                    if vals['motivation']:
                        vals2 = {
                            'body': '<p>' + u'' + vals['motivation'] + '</p>',
                            'model': 'stock.picking',
                            # 'record_name':picking_data.name,
                            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'author_id': user.partner_id.id,
                            'res_id': ids[0],
                            'type': 'comment',
                        }
                        self.env['mail.message'].create(vals2)
                        vals['date_changed'] = False
                        vals['motivation'] = False
                    else:
                        raise self.env.osv.except_osv(('Erreur'), ('Veuillez saisir la motivation de votre modification'))
                else:
                    raise self.env.osv.except_osv(('Erreur'), ('Veuillez saisir la motivation de votre modification'))

        super(stock_picking, self).write(vals)

        return True



