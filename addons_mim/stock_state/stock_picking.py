# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _columns = {
                'confirmed':fields.char(u'Attente de disponibilité',size=20,help=u'Attente de disponibilité'),
                'contre_mesure': fields.char('Contre mesure',size=20, help="Contre mesure"),
                'fiche_debit': fields.char(u'Fiche de débit',size=20, help=u"Fiche de débit"),
                'assigned': fields.char('Disponible',size=20, help="Disponible"),
                'done': fields.char(u'Terminé',size=20, help=u'Terminé'),
                'total':fields.char('Total',size=20, help='Total'),
                }
    def refresh(self, cr, uid, ids, context=None):
        res = { 'type': 'ir.actions.client', 'tag': 'reload' }
        tname=[]
        cr.execute("SELECT DISTINCT sp.name FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.picking_type_id='2'")
        resultat=cr.fetchall()
        
        #if resultat[0]!=None:
        #for row_name in resultat: 
            #tname.append(row_name[0])
            
        for x in range(len(resultat)):
            tname.append(resultat[x][0])
    
        for n in tname:
            query_total="SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}'".format(str(n))
            query_confirmed="SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='confirmed'".format(str(n))
            query_contre_mesure="SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='contre_mesure'".format(str(n))
            query_fiche_debit="SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='flowsheeting'".format(str(n))
            query_assigned="SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='assigned'".format(str(n))
            query_done="SELECT SUM(sm.product_qty) FROM stock_picking sp INNER JOIN stock_move sm ON sp.id = sm.picking_id WHERE sp.name='{0}' AND sm.state='done'".format(str(n))
            
            cr.execute(query_total)
            total=cr.dictfetchone()
            
            cr.execute(query_confirmed)
            confirmed=cr.dictfetchone()
            
            cr.execute(query_contre_mesure)
            contre_mesure=cr.dictfetchone()
            
            cr.execute(query_fiche_debit)
            fiche_debit=cr.dictfetchone()
            
            cr.execute(query_assigned)
            assigned=cr.dictfetchone()
            
            cr.execute(query_done)
            done=cr.dictfetchone()
            
            if (confirmed["sum"]==None):
                confirmed["sum"]= 0.0
                
            if (contre_mesure["sum"]==None) :
                contre_mesure["sum"]= 0.0
                
            if (fiche_debit["sum"]==None) :
                fiche_debit["sum"]= 0.0
                
            if (assigned["sum"]==None) :
                assigned["sum"]= 0.0
                
            if (done["sum"]==None) :
                done["sum"]= 0.0
                
            if (total["sum"]==None):
                total["sum"]= 0.0
            
            confirmed5 = confirmed["sum"] + contre_mesure["sum"] + fiche_debit["sum"] + assigned["sum"] + done["sum"]
            contre_mesure5 = contre_mesure["sum"] + fiche_debit["sum"] + assigned["sum"] + done["sum"]
            fiche_debit5 = fiche_debit["sum"] + assigned["sum"] + done["sum"]
            assigned5 = assigned["sum"] + done["sum"]
            done5 = done["sum"]
            total5 = total["sum"]
            
            confirmed3=int(confirmed5)
            contre_mesure3=int(contre_mesure5)
            fiche_debit3=int(fiche_debit5)
            assigned3=int(assigned5)
            done3=int(done5)
            total3=int(total5)
            
            confirmed2=str(confirmed3) + '/' + str(total3)
            
            
            contre_mesure2=str(contre_mesure3) + '/' + str(total3)
            
            
            fiche_debit2=str(fiche_debit3) + '/' + str(total3)
            
            
            assigned2=str(assigned3) + '/' + str(total3)
            
            
            done2=str(done3) + '/' + str(total3)
            
            query_update_confirmed="UPDATE stock_picking sp SET confirmed = '{0}' WHERE sp.name = '{1}'".format(confirmed2,str(n))
            query_update_contre_mesure="UPDATE stock_picking sp SET contre_mesure = '{0}' WHERE sp.name = '{1}'".format(contre_mesure2,str(n))
            query_update_fiche_debit="UPDATE stock_picking sp SET fiche_debit = '{0}' WHERE sp.name = '{1}'".format(fiche_debit2,str(n))
            query_update_assigned="UPDATE stock_picking sp SET assigned = '{0}' WHERE sp.name = '{1}'".format(assigned2,str(n))
            query_update_done="UPDATE stock_picking sp SET done = '{0}' WHERE sp.name = '{1}'".format(done2,str(n))
            
            cr.execute(query_update_confirmed)
            cr.execute(query_update_contre_mesure)
            cr.execute(query_update_fiche_debit)
            cr.execute(query_update_assigned)
            cr.execute(query_update_done)
            
        return res
    
stock_picking()