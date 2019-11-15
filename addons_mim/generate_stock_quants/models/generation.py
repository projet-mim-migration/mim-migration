# -*- coding: utf-8 -*-

from odoo import models, fields, api


class generation(models.Model):
	_name ="generation.models"
	
	visible = fields.Boolean("Visible",default=False)
	

	def get_stockmovedone(self):
		self.env.cr.execute("SELECT id from stock_move where state='done' order by date ASC") 
		liste_move_done =[]
		res = self.env.cr.fetchall()
		for i in range(len(res)):
			liste_move_done.append(res[i][0])
		return liste_move_done
	
	def get_id_wkf_workitem(self): 
		self.env.cr.execute("select distinct(wkf_workitem.id)  from wkf_workitem \
		where inst_id in (select distinct(wkf_instance.id) from stock_move\
		inner join wkf_instance\
		on stock_move.id=wkf_instance.res_id \
		where stock_move.state='done'\
		and wkf_instance.res_type='stock.move')")
		res = self.env.cr.fetchall()
	   
		liste_wkf_work=[]
		for i in range(len(res)):
			liste_wkf_work.append(res[i][0])
		   
			
		return liste_wkf_work
	
	def get_id_wkf_inst(self): 
		self.env.cr.execute("select distinct(wkf_instance.id) from stock_move \
		inner join wkf_instance on stock_move.id=wkf_instance.res_id \
		where stock_move.state='done' and wkf_instance.res_type='stock.move'")
		res = self.env.cr.fetchall()
		liste_wkf_inst=[]
	   
		for i in range(len(res)):
			
			liste_wkf_inst.append(res[i][0])
			
		return liste_wkf_inst
	

	def update_leisyah(self):
		liste1= self.get_id_wkf_inst()
		liste2= self.get_id_wkf_workitem()
		liste_stockmove =self.get_stockmovedone()
		for t in liste_stockmove:
			self.env.cr.execute("UPDATE stock_move SET state ='assigned' where id={}".format(t))
		
		for i in liste1:
			self.env.cr.execute("UPDATE  wkf_instance SET state='active' \
			where id={} ".format(i))
		
		for j in liste2:
			self.env.cr.execute("UPDATE wkf_workitem SET act_id=62 \
			where id={} ".format(j))   
		
		
		for r in liste_stockmove:
				#netsvc.LocalService("workflow").trg_validate(SUPERUSER_ID, 'stock.move', r, 'action_done', cr)
				self.env['stock.move'].action_done(r)
				 
				
		gener_obj = self.env['generation.models']
		gener_obj.search([('id','=',self.ids[0])]).write({'visible':True})
		