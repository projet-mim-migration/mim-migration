from openerp.osv import fields, osv

class account_voucher(osv.osv):
    
    def _get_user_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('user_id', False)
    _inherit = 'account.voucher'
    _columns = {
                'user_id': fields.many2one('res.users', 'Vendeur', readonly=True)
                }
    
    _defaults = {
                 'user_id':_get_user_id,
                 #'user_id': lambda s, cr, uid, c: s._get_default_user(cr, uid, c),
                 }
    #def _get_default_user(self, cr, uid, context=None):
        #return uid'''
    
    def refresh(self, cr, uid, ids, context=None):
        origin="SELECT account_invoice.origin FROM account_invoice WHERE account_invoice.state='paid' ORDER BY account_invoice.id asc"
        user_id="SELECT account_invoice.user_id FROM account_invoice WHERE account_invoice.state='paid' ORDER BY account_invoice.id asc"
        t_origin=[]
        t_user_id=[]
        
        cr.execute(origin)
        res_origin=cr.fetchall()
        for a in range(len(res_origin)):
            t_origin.append(res_origin[a][0])
            
        cr.execute(user_id)
        res_user_id=cr.fetchall()
        for b in range(len(res_user_id)):
            t_user_id.append(res_user_id[b][0])
        
        for c in range(len(t_origin)):
            if (t_user_id[c]!=None and t_origin[c]!=None):
                query="UPDATE account_voucher av SET user_id = {0} WHERE av.reference LIKE '%{1}%'".format(t_user_id[c],t_origin[c])
                cr.execute(query)
        res = { 'type': 'ir.actions.client', 'tag': 'reload' }
        return res  
        
account_voucher()








