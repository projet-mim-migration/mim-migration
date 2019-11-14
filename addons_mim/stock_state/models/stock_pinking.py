# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_picking(models.Model):
    _inherit = 'stock.picking'

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


