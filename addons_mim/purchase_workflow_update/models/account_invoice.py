# -*- coding: utf-8 -*-

from odoo import fields, models, exceptions, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    @api.multi
    def action_invoice_open(self):
        super(AccountInvoice, self).action_invoice_open()
        self.invoice_validate2()

    @api.multi
    def invoice_validate2(self):
        type_journal = self.journal_id.type
        if type_journal=='purchase':
            po = self.env['purchase.order']
            origin = self.origin
            self.env.cr.execute("""SELECT purchase_order.id 
                                   FROM purchase_order 
                                   WHERE purchase_order.name='{0}'""".format(origin)
            )
            res1 = self.env.cr.fetchone()
            self.env.cr.execute("""SELECT ir_attachment.datas_fname 
                                   FROM ir_attachment 
                                   WHERE ir_attachment.res_id={0}""".format(self.id)
            )
            res2 = self.env.cr.fetchall()
            liste_name = []
            name_invoice = "Facture_"+origin
    
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
                    raise exceptions.UserError(u"Aucune pièce jointe n'a un nom correcte")
            else:
                raise exceptions.UserError(u"Aucune pièce jointe n'a été ajoutée")         
            test = test3
            if res1:
                if res1[0]:
                    if test:
                        id_po=[]
                        id_po.append(res1[0])
                        po.wkf_recept_invoice(id_po)
            else: 
                raise exceptions.UserError(u"Cette facture n'a pas de document d'origine")           
        return True