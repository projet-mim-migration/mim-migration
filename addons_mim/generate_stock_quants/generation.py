from openerp.osv import osv,fields
from openerp import SUPERUSER_ID
from openerp import netsvc

class generation(osv.osv):
    _name ="generation.models"
    _columns={
              "visible":fields.boolean("Visible")
              
              }
    _defaults={
               'visible':False
               }
    def get_stockmovedone(self,cr ,uid ,ids, Context=None):
        cr.execute("SELECT id from stock_move where state='done' order by date ASC") 
        liste_move_done =[]
        res = cr.fetchall()
        for i in range(len(res)):
            liste_move_done.append(res[i][0])
        return liste_move_done
    
    def get_id_wkf_workitem(self,cr ,uid,ids ,Context=None): 
        cr.execute("select distinct(wkf_workitem.id)  from wkf_workitem \
        where inst_id in (select distinct(wkf_instance.id) from stock_move\
        inner join wkf_instance\
        on stock_move.id=wkf_instance.res_id \
        where stock_move.state='done'\
        and wkf_instance.res_type='stock.move')")
        res=cr.fetchall()
       
        liste_wkf_work=[]
        for i in range(len(res)):
            liste_wkf_work.append(res[i][0])
           
            
        return liste_wkf_work
    
    def get_id_wkf_inst(self,cr ,uid,ids ,Context=None): 
        cr.execute("select distinct(wkf_instance.id) from stock_move \
        inner join wkf_instance on stock_move.id=wkf_instance.res_id \
        where stock_move.state='done' and wkf_instance.res_type='stock.move'")
        res=cr.fetchall()
        liste_wkf_inst=[]
       
        for i in range(len(res)):
            
            liste_wkf_inst.append(res[i][0])
            
        return liste_wkf_inst
    
    def update_leisyah(self,cr,uid,ids,Context=None):
        liste1= self.get_id_wkf_inst(cr, uid, ids, Context)
        liste2= self.get_id_wkf_workitem(cr, uid, ids, Context)
        liste_stockmove =self.get_stockmovedone(cr,uid,ids,Context)
        for t in liste_stockmove:
            cr.execute("UPDATE stock_move SET state ='assigned' where id={}".format(t))
        
        for i in liste1:
            cr.execute("UPDATE  wkf_instance SET state='active' \
            where id={} ".format(i))
        
        for j in liste2:
            cr.execute("UPDATE wkf_workitem SET act_id=62 \
            where id={} ".format(j))   
        
        
        for r in liste_stockmove:
                #netsvc.LocalService("workflow").trg_validate(SUPERUSER_ID, 'stock.move', r, 'action_done', cr)
                self.pool.get('stock.move').action_done(cr, uid,r, context=Context)
                 
                
        gener_obj = self.pool.get('generation.models')
        gener_obj.write(cr,uid, [ids[0]] , {'visible':True}, context=Context)