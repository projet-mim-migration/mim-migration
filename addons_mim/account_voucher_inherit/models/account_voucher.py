# -*- coding: utf-8 -*-

from odoo import models, fields, api

class account_voucher(models.Model):
    
    _inherit = 'account.voucher'
    
    def _get_user_id(self):
        if self.env.context is None: self.env.context = {}
        return self.env.context.get('user_id', False)
    

    user_id = fields.Many2one('res.users', 'Vendeur', readonly=True, default=_get_user_id)
    
    #def _get_default_user(self, cr, uid, context=None):
        #return uid'''
    
    def refresh(self):
        origin = "SELECT account_invoice.origin FROM account_invoice WHERE account_invoice.state='paid' ORDER BY account_invoice.id asc"
        user_id = "SELECT account_invoice.user_id FROM account_invoice WHERE account_invoice.state='paid' ORDER BY account_invoice.id asc"
        t_origin = []
        t_user_id = []
        
        self.env.cr.execute(origin)
        res_origin = self.env.cr.fetchall()
        for a in range(len(res_origin)):
            t_origin.append(res_origin[a][0])
            
        self.env.cr.execute(user_id)
        res_user_id = self.env.cr.fetchall()
        for b in range(len(res_user_id)):
            t_user_id.append(res_user_id[b][0])
        
        for c in range(len(t_origin)):
            if (t_user_id[c]!=None and t_origin[c]!=None):
                query="UPDATE account_voucher av SET user_id = {0} WHERE av.reference LIKE '%{1}%'".format(t_user_id[c],t_origin[c])
                self.env.cr.execute(query)
        res = { 'type': 'ir.actions.client', 'tag': 'reload' }
        return res  
 