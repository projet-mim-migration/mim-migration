# -*- coding: utf-8 -*-

import time
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, api, exceptions


class StockPicking(models.Model):
    _inherit = "stock.picking"
    

    @api.depends('date')
    def _get_late_production(self):
        res = {}
        fmt_datetime = DEFAULT_SERVER_DATETIME_FORMAT
        fmt_date = DEFAULT_SERVER_DATE_FORMAT
        
        for pick in self:
            if not pick.date:
                pick.late_production = False
                continue
            if pick.is_old_picking_assigned:
                pick.late_production = False
                continue
    
            date_delivery = str(pick.date)
            date_reference = str(datetime.now().strftime(fmt_datetime))
            if pick.production_date:
                date_reference = str(pick.production_date)
            
            d1 = datetime.strptime(str(datetime.strptime(date_reference, fmt_datetime).date()), fmt_date) 
            d2 = datetime.strptime(str(datetime.strptime(date_delivery, fmt_datetime).date()), fmt_date)  
            diff_date = d1 - d2
            days = diff_date.days
            pick.late_production = days


    @api.depends('date')
    def _get_late_delivery(self):
        res = {}
        fmt_datetime = DEFAULT_SERVER_DATETIME_FORMAT
        fmt_date = DEFAULT_SERVER_DATE_FORMAT
        
        for pick in self:
            if not pick.date:
                pick.late_delivery = False
                continue
            
            if pick.is_old_picking_done:
                pick.late_delivery = False
                continue
    
            date_delivery = str(pick.date)
            date_reference = str(datetime.now().strftime(fmt_datetime))
            if pick.delivery_date:
                date_reference = str(pick.delivery_date)
            
            d1 = datetime.strptime(str(datetime.strptime(date_reference, fmt_datetime).date()), fmt_date) 
            d2 = datetime.strptime(str(datetime.strptime(date_delivery, fmt_datetime).date()), fmt_date)  
            diff_date = d1 - d2
            days = diff_date.days
            pick.late_delivery = days

    
    @api.depends('move_lines')
    def _get_mo_created(self):        
        for pick in self:
            pick.mo_created_copy = pick.mo_created = False

            if any(move.id_mo for move in pick.move_lines):
                pick.mo_created_copy = pick.mo_created = True

    # # Added because the product is "assingned" - changed with "confirmed"
    # @api.onchange('state')
    # def _onchange_state(self):
    #     print("state onchange: {}".format(self.state))
            


    # Added because error when passed in "contre mesure"
    def _compute_state(self):
        super(StockPicking, self)._compute_state()     

        for pick in self:                
            if pick.state == 'contre_mesure' or pick.state == 'flowsheeting' or (pick.show_check_availability and pick.state == 'assigned'):
                pick.state = 'confirmed'


    state = fields.Selection(
        [('draft', 'Draft'),
         ('waiting', 'Waiting Another Operation'),
         ('confirmed', 'Waiting'),
         ('contre_mesure', 'Contre mesure'),
         ('flowsheeting', u'Fiche de Débit'),
         ('assigned', 'Ready'),
         ('done', 'Done'),
         ('cancel', 'Cancelled')], 
        string='Status',
        readonly=True, 
        track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed.\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows).\n"
             " * Waiting: if it is not ready to be sent because the required products could not be reserved.\n"
             " * Ready: products are reserved and ready to be sent. If the shipping policy is 'As soon as possible' this happens as soon as anything is reserved.\n"
             " * Done: has been processed, can't be modified or cancelled anymore.\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore."
    )

    # Fields for the interaction with MRP
    mo_created = fields.Boolean(
        string=u'Ordre de fabrication créé', 
        store=False,
        compute=_get_mo_created
    )
    late_production = fields.Float(
        string='Retard de production (jours)',
        compute=_get_late_production
    )
    production_date = fields.Datetime(
        'Date de fin production', 
        readonly=True
    )
    late_delivery = fields.Float(
        string='Retard de livraison (jours)', 
        compute=_get_late_delivery
    )
    delivery_date = fields.Datetime(
        'Date de fin livraison', 
        readonly=True
    )
    is_old_picking_assigned = fields.Boolean(
        u'Ancien BL disponible',
        default=False
    )
    is_old_picking_done = fields.Boolean(
        u'Ancien BL terminé',
        default=False
    )
    mo_created_copy = fields.Boolean(
        string=u'Ordre de fabrication créé ?'
    )

    min_date = fields.Datetime(
        'Date de contre-mesure', 
        help="Date de contre-mesure", 
        states={'done':[('readonly', True)], 'cancel':[('readonly',True)]}, 
        default= lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    )
    date = fields.Datetime(
        'Date de livraison', 
        help="Date de livraison", 
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, 
        default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    )
    motivation = fields.Text(
        'Motivation'
    )
    date_changed = fields.Boolean(
        'Date changée', 
        default=False
    )
    confirmed = fields.Char(
        'Attente de disponibilité', 
        size=20, 
        help='Attente de disponibilité'
    )
    contre_mesure = fields.Char(
        'Contre mesure', 
        size=20, 
        help="Contre mesure"
    )
    fiche_debit = fields.Char(
        'Fiche de débit', 
        size=20, 
        help="Fiche de débit"
    )
    assigned = fields.Char(
        'Disponible', 
        size=20, 
        help="Disponible"
    )
    done = fields.Char(
        'Terminé', 
        size=20, 
        help='Terminé'
    )
    total = fields.Char(
        'Total', 
        size=20, 
        help='Total'
    )


    @api.cr_uid_ids_context
    def split_picking(self, picking):
        ctx = {
            'active_model': self._name,
            'active_ids': picking['active_ids'],
            'active_id': picking['active_id'],
            'do_only_split': True,
        }

        self = self.with_context(ctx)
        
        created_id = self.env['stock.split_details'].create({'picking_id': picking['active_id']})
        
        return self.env['stock.split_details'].browse(created_id).wizard_view()
    

    @api.multi
    def confirm_config_mo(self):
        self.ensure_one()
        
        ctx = dict()
        ctx.update({
            'default_picking_source_id': self.id,
            'default_date_planned': self.date,
        })
        return {
            'name': u'Veuillez entrer la date prévue',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.configuration',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }
    

    @api.multi
    def view_all_mo(self):
        self.ensure_one()

        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        result = mod_obj.get_object_reference('mrp', 'mrp_production_action')
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]

        mo_ids = [p.id_mo for p in self.move_lines if p.id_mo]
        if len(mo_ids) < 1:
            return {}       
        else: 
            if len(mo_ids) > 1:
                result['domain'] = "[('id','in',["+','.join(map(str, mo_ids))+"])]"
            else:
                res = mod_obj.get_object_reference('mrp', 'mrp_production_form_view')
                result['views'] = [(res and res[1] or False, 'form')]
                result['res_id'] = mo_ids and mo_ids[0] or False
        
        return result


    def refresh(self):
        res = {'type': 'ir.actions.client', 'tag': 'reload'}
        tname = []
        self._cr.execute("""SELECT DISTINCT sp.name 
                            FROM stock_picking sp 
                            INNER JOIN stock_move sm 
                            ON sp.id = sm.picking_id 
                            WHERE sp.picking_type_id='2'""")
        resultat = self._cr.fetchall()

        for x in range(len(resultat)):
            tname.append(resultat[x][0])

        for n in tname:
            query_total = """SELECT SUM(sm.product_qty) 
                             FROM stock_picking sp 
                             INNER JOIN stock_move sm 
                             ON sp.id = sm.picking_id 
                             WHERE sp.name='{0}'""".format(str(n))
            query_confirmed = """SELECT SUM(sm.product_qty) 
                                 FROM stock_picking sp 
                                 INNER JOIN stock_move sm 
                                 ON sp.id = sm.picking_id 
                                 WHERE sp.name='{0}' 
                                 AND sm.state='confirmed'""".format(str(n))
            query_contre_mesure = """SELECT SUM(sm.product_qty) 
                                     FROM stock_picking sp 
                                     INNER JOIN stock_move sm 
                                     ON sp.id = sm.picking_id 
                                     WHERE sp.name='{0}' 
                                     AND sm.state='contre_mesure'""".format(str(n))
            query_fiche_debit = """SELECT SUM(sm.product_qty) 
                                   FROM stock_picking sp 
                                   INNER JOIN stock_move sm 
                                   ON sp.id = sm.picking_id 
                                   WHERE sp.name='{0}' 
                                   AND sm.state='flowsheeting'""".format(str(n))
            query_assigned = """SELECT SUM(sm.product_qty) 
                                FROM stock_picking sp 
                                INNER JOIN stock_move sm 
                                ON sp.id = sm.picking_id 
                                WHERE sp.name='{0}' 
                                AND sm.state='assigned'""".format(str(n))
            query_done = """SELECT SUM(sm.product_qty) 
                            FROM stock_picking sp 
                            INNER JOIN stock_move sm 
                            ON sp.id = sm.picking_id 
                            WHERE sp.name='{0}' 
                            AND sm.state='done'""".format(str(n))

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
        if self.ids != None:
            self.date_changed = True
        else:
            self.date_changed = False

    @api.multi
    def write(self, vals):
        user_obj = self.env['res.users']

        if self.date_changed:
            if self.date_changed == True:
                if 'motivation' in vals:
                    if vals['motivation']:
                        vals2 = {
                            'body': '<p>' + u'' + vals['motivation'] + '</p>',
                            'model': 'stock.picking',
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

        super(StockPicking, self).write(vals)

        return True

    
    #@api.depends('pick.move_lines', 'x.state', 'move.partially_available')
    @api.multi
    def _state_get_new(self, field_name, arg):
        '''The state of a picking depends on the state of its related stock.move
            draft: the picking has no line or any one of the lines is draft
            done, draft, cancel: all lines are done / draft / cancel
            confirmed, waiting, assigned, partially_available depends on move_type (all at once or partial)
        '''
        res = {}
        for pick in self:
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

    @api.multi
    def _get_pickings(self):
        res = set()
        for move in self:
            if move.picking_id:
                res.add(move.picking_id.id)
        return list(res)

    # Make the product unavaillable 
    # @api.model
    # def create(self, values):
    #     pick = super(StockPicking, self).create(values)
    #     print("\nstock_picking\n")
    #     print(pick)
    #     print(pick.state)
    #     return pick