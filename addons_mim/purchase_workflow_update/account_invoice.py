# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    def invoice_validate2(self, cr, uid, ids, context=None):
        type_journal = self.browse(cr, uid, ids, context=context)[0].journal_id.type
        if type_journal=='purchase':
            po = self.pool.get('purchase.order')
            origin = self.browse(cr, uid, ids, context=context)[0].origin
            cr.execute("""select purchase_order.id from purchase_order where purchase_order.name='{0}'""".format(origin))
            res1 = cr.fetchone()
            cr.execute("""select ir_attachment.datas_fname from ir_attachment where ir_attachment.res_id={0}""".format(ids[0]))
            res2 = cr.fetchall()
            liste_name = []
            name_invoice = "Facture_"+origin
            #test1 = False
            #test2 = False
            test3 = False
            if res2:
                for x in range(len(res2)):
                    if res2[x][0]:
                        liste_name.append(res2[x][0])
                for y in range(len(liste_name)):
                    liste_name2 = liste_name[y].split('.')[0]
                    if liste_name2==name_invoice:
                        test2 = True
                    else : test2 = False
                    test3 = test3 or test2
                if not test3:             
                    raise osv.except_osv(('Erreur'), (u'Aucune pièce jointe n\'a un nom correcte'))
            else:
                raise osv.except_osv(('Erreur'), (u'Aucune pièce jointe n\'a été ajoutée'))         
            test = test3
            if res1:
                if res1[0]:
                    if test:
                        id_po=[]
                        id_po.append(res1[0])
                        po.wkf_recept_invoice(cr, uid, id_po, context)
            else: 
                raise osv.except_osv(('Erreur'), (u'Cette facture n\'a pas de document d\'origine'))           
        return True
account_invoice()
    