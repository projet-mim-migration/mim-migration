# -*- coding: utf-8 -*-

import time
from datetime import datetime

from odoo import models, fields, api, exceptions


class stock_move(models.Model):

    _inherit = 'stock.move'
    
    '''def action_done(self):
                  if self.state in ['draft','assigned','cancel','contre_mesure','confirmed','flowsheeting']:
                    self._action_done()
                  else:
                    pass
                    
                def action_confirm(self):
                  if self.state in ['draft','cancel']:
                    #self.state = 'confirmed'
                    self._action_confirm()
                  else:
                    pass
            '''
    def contre_mesure1(self):
      if self.state in ['draft','confirmed']:
        self.state = 'contre_mesure'
      else:
        pass

    def annuler_contre_mesure(self):
      
      if self.state == 'contre_mesure':
        self.state = 'confirmed'
      else:
        pass

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


    def force_assign(self):
      if self.state == 'flowsheeting':
        self.state = 'assigned'
      else:
        pass


    state = fields.Selection([('draft', 'New'),
                               ('cancel', 'Cancelled'),
                               ('waiting', 'Waiting Another Move'),
                               ('confirmed', 'Waiting Availability'),
                               ('contre_mesure', 'Contre mesure'),
                               ('flowsheeting', u'Fiche de Débit'),
                               ('assigned', 'Available'),
                               ('done', 'Done'),
                               ], 'Status', readonly=True, select=True,
                              help="* New: When the stock move is created and not yet confirmed.\n" \
                                   "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n" \
                                   "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to me manufactured...\n" \
                                   "* Fiche de Debit: the state is \'Fiche de Debit\'.\n"
                                   "* Available: When products are reserved, it is set to \'Available\'l.\n" \
                                   "* Done: When the shipment is processed, the state is \'Done\'.")

   

    date_prevue = fields.Datetime('Date prevue', help="Date prevue", select=True,
                               states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                               default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    min_date = fields.Datetime('Date de contre-mesure', help="Date de contre-mesure", select=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    date = fields.Datetime('Date de livraison', help="Date de livraison", select=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))



class stock_picking(models.Model):
    _inherit = "stock.picking"
    
    min_date = fields.Datetime('Date de contre-mesure', help="Date de contre-mesure", select=True, states={'done':[('readonly', True)], 'cancel':[('readonly',True)]}, default= lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    date = fields.Datetime('Date de livraison', help="Date de livraison", select=True, states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))

    motivation = fields.Text('Motivation')
    date_changed = fields.Boolean('Date changée', default=False)

    confirmed = fields.Char('Attente de disponibilité', size=20, help='Attente de disponibilité')
    contre_mesure = fields.Char('Contre mesure', size=20, help="Contre mesure")
    fiche_debit = fields.Char('Fiche de débit', size=20, help="Fiche de débit")
    assigned = fields.Char('Disponible', size=20, help="Disponible")
    done = fields.Char('Terminé', size=20, help='Terminé')
    total = fields.Char('Total', size=20, help='Total')

    def refresh(self):
        res = {'type': 'ir.actions.client', 'tag': 'reload'}
        tname = []
        self._cr.execute("SELECT DISTINCT sp.name FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.picking_type_id='2'")
        resultat = self._cr.fetchall()

        # if resultat[0]!=None:
        # for row_name in resultat:
        # tname.append(row_name[0])

        for x in range(len(resultat)):
            tname.append(resultat[x][0])

        for n in tname:
            query_total = "SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}'".format(
                str(n))
            query_confirmed = "SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='confirmed'".format(
                str(n))
            query_contre_mesure = "SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='contre_mesure'".format(
                str(n))
            query_fiche_debit = "SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='flowsheeting'".format(
                str(n))
            query_assigned = "SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='assigned'".format(
                str(n))
            query_done = "SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='done'".format(
                str(n))

            self._cr.execute(query_total)
            total = self._cr.dictfetchone()

            self._cr.execute(query_confirmed)
            confirmed = self._cr.dictfetchone()

            self._cr.execute(query_contre_mesure)
            contre_mesure = self._cr.dictfetchone()

            self._cr.execute(query_fiche_debit)
            fiche_debit = self._cr.dictfetchone()

            self._cr.execute(query_assigned)
            assigned = self._cr.dictfetchone()

            self._cr.execute(query_done)
            done = self._cr.dictfetchone()

            if (confirmed["sum"] == None):
                confirmed["sum"] = 0.0

            if (contre_mesure["sum"] == None):
                contre_mesure["sum"] = 0.0

            if (fiche_debit["sum"] == None):
                fiche_debit["sum"] = 0.0

            if (assigned["sum"] == None):
                assigned["sum"] = 0.0

            if (done["sum"] == None):
                done["sum"] = 0.0

            if (total["sum"] == None):
                total["sum"] = 0.0

            confirmed5 = confirmed["sum"] + contre_mesure["sum"] + fiche_debit["sum"] + assigned["sum"] + done["sum"]
            contre_mesure5 = contre_mesure["sum"] + fiche_debit["sum"] + assigned["sum"] + done["sum"]
            fiche_debit5 = fiche_debit["sum"] + assigned["sum"] + done["sum"]
            assigned5 = assigned["sum"] + done["sum"]
            done5 = done["sum"]
            total5 = total["sum"]

            confirmed3 = int(confirmed5)
            contre_mesure3 = int(contre_mesure5)
            fiche_debit3 = int(fiche_debit5)
            assigned3 = int(assigned5)
            done3 = int(done5)
            total3 = int(total5)

            confirmed2 = str(confirmed3) + '/' + str(total3)

            contre_mesure2 = str(contre_mesure3) + '/' + str(total3)

            fiche_debit2 = str(fiche_debit3) + '/' + str(total3)

            assigned2 = str(assigned3) + '/' + str(total3)

            done2 = str(done3) + '/' + str(total3)

            query_update_confirmed = "UPDATE stock_picking sp SET confirmed = '{0}' WHERE sp.name = '{1}'".format(
                confirmed2, str(n))
            query_update_contre_mesure = "UPDATE stock_picking sp SET contre_mesure = '{0}' WHERE sp.name = '{1}'".format(
                contre_mesure2, str(n))
            query_update_fiche_debit = "UPDATE stock_picking sp SET fiche_debit = '{0}' WHERE sp.name = '{1}'".format(
                fiche_debit2, str(n))
            query_update_assigned = "UPDATE stock_picking sp SET assigned = '{0}' WHERE sp.name = '{1}'".format(
                assigned2, str(n))
            query_update_done = "UPDATE stock_picking sp SET done = '{0}' WHERE sp.name = '{1}'".format(done2, str(n))

            self._cr.execute(query_update_confirmed)
            self._cr.execute(query_update_contre_mesure)
            self._cr.execute(query_update_fiche_debit)
            self._cr.execute(query_update_assigned)
            self._cr.execute(query_update_done)

        return res



    
    # Evenement losrque la date de livraison est modifié
    @api.onchange('date')
    def onchange_fields(self):
        #return {'value': {'date_changed': True}}
        if self.ids != None:
            self.date_changed = True
        else:
            self.date_changed = False

    @api.multi
    def write(self, vals):
        # picking_data = self.browse(cr, uid, ids, context=context)[0]
        user_obj = self.env['res.users']
        # uids = user_obj.search(cr, uid, [('id','=',uid)], context=context)
        user = user_obj.browse()
        if self.date_changed:
            if self.date_changed == True:
                if 'motivation' in vals:
                    if vals['motivation']:
                        vals2 = {
                            'body': '<p>' + u'' + vals['motivation'] + '</p>',
                            'model': 'stock.picking',
                            # 'record_name':picking_data.name,
                            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'author_id': self.env.user.partner_id.id,
                            'res_id': self.ids[0],
                            'type': 'comment',
                        }
                        self.env['mail.message'].create(vals2)
                        vals['date_changed'] = False
                        vals['motivation'] = False
                    else:
                        raise exceptions.Warning(('Veuillez saisir la motivation de votre modification'))
                else:
                    raise exceptions.Warning(('Veuillez saisir la motivation de votre modification'))

        super(stock_picking, self).write(vals)

        return True



    def contre_mesure1(self):
      if self.state in ['draft','confirmed']:
        self.state = 'contre_mesure'
      else:
        pass

    def annuler_contre_mesure(self):
      
      if self.state == 'contre_mesure':
        self.state = 'confirmed'
      else:
        pass

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

    def force_assign(self):
      if self.state == 'flowsheeting':
        self.state = 'assigned'
      else:
        pass
    
    #@api.depends('pick.move_lines', 'x.state', 'move.partially_available')
    @api.one
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

    
   