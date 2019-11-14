# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    paiement_etabli = fields.Char(
        u'Paiement établi'
    )
    facture_recue = fields.Char(
        u'Facture reçue'
    )
    
    @api.multi
    def payement_not_ok(self):
        self.write({'paiement_etabli': ''})
        return True
    
    @api.multi
    def payement_ok(self):
        self.write({'paiement_etabli': 'Oui'})
        return True

    @api.multi
    def wkf_recept_invoice(self):
        self.write({'facture_recue': 'Oui'})
        return True

   
    @api.multi
    def get_list_id_jump_wkf(self):
        self._cr.execute('''SELECT product_category.id 
                            FROM product_category 
                            WHERE product_category.confirmed_wkf_ok = 0''')
        res = self._cr.fetchall()
        list_id = []
        for x in range(len(res)):
            list_id.append(res[x][0])
        return list_id

    @api.multi
    def jump_confirmed(self):
        tres = []
        for purchase in self:
            for line in purchase.order_line:
                if line:
                    tres.append(line.product_id.categ_id.id)
        
        categ_article = self.get_list_id_jump_wkf()
        res_bool = 1
        res_test = 1  
        for t in tres:
            if t in categ_article :
                res_bool = 1
            else:res_bool = 0
            res_test *= res_bool
        state = self.state
        if (res_test == 1 and state in ['draft','sent']):
            self.button_confirm()
        return True

    @api.model
    def create(self, vals):
        #appel de la fonction de la classe mere
        res_id = super(PurchaseOrder, self).create(vals)
        #Ajout code redefiniton
        self.jump_confirmed()
        return res_id

    @api.model
    def write(self, vals):
        #appel de la fonction de la classe mere
        super(PurchaseOrder, self).write(vals)
        #Ajout code redefiniton
        self.jump_confirmed()
        return True