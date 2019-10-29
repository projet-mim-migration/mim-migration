
# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    @api.model
    def _get_user_id(self):
        context = self._context or {}
        return context.get('user_id', False)
    
    
    user_id = fields.Many2one(
        'res.users', 
        'Vendeur', 
        readonly=True,
        default=_get_user_id
    )
    
    @api.multi
    def refresh(self):
        origin =" SELECT account_invoice.origin FROM account_invoice WHERE account_invoice.state='paid' ORDER BY account_invoice.id asc"
        user_id = "SELECT account_invoice.user_id FROM account_invoice WHERE account_invoice.state='paid' ORDER BY account_invoice.id asc"
        t_origin = []
        t_user_id = []
        
        self._cr.execute(origin)
        res_origin = self._cr.fetchall()
        for a in range(len(res_origin)):
            t_origin.append(res_origin[a][0])
            
        self._cr.execute(user_id)
        res_user_id = self._cr.fetchall()
        for b in range(len(res_user_id)):
            t_user_id.append(res_user_id[b][0])
        
        for c in range(len(t_origin)):
            if (t_user_id[c] != None and t_origin[c]!=None):
                query = "UPDATE account_voucher av SET user_id = {0} WHERE av.reference LIKE '%{1}%'".format(t_user_id[c],t_origin[c])
                self._cr.execute(query)
        res = { 'type': 'ir.actions.client', 'tag': 'reload' }
        return res  
        

