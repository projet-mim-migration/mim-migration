# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo import tools, modules
import base64

class mim_wizard(models.TransientModel):
	"""  """
	_inherit = 'mim.wizard'
	'''
	def _get_order_id(self):
		if context is None: context = {}
		return context.get('order_id', False)
	'''
	image = fields.Binary('Image')
	order_id = fields.Integer('Order Lines') #,default=_get_order_id()
	
	
	####cette fonction permet la crÃ©ation d'une ligne de commande grÃ¢ce Ã  sale_order_line_obj.create(cr, uid, {'name': name,'order_id':rec_ref, 'price_unit' : rec_total})####
	def order_line_create(self):
		print('######################################################################')
		print('######################################################################')
		print('##ADD IMAGE##')
		print('######################################################################')
		print('######################################################################')
		
		sale_order_line_obj = self.env['sale.order.line']#on recupÃ¨re l'objet sale.order.line pour l'utiliser avec la fonction ORM create 
		#### dÃ©but de la rÃ©cupÃ¨ration des diffÃ©rents paramÃ¨tres saisi sur le pop-up####
		select_type = self.select_type
		type_fix = self.type_fixe
		inegalite = self.inegalite
		vitrage = self.vitre
		type_vitre = self.type_vitre
		decoratif = self.decoratif
		serr = self.serr
		poigne = self.poigne
		nb_poigne = self.nb_poigne
		nb_serr = self.nb_serr
		oscillo_battant = self.oscillo_battant
		va_et_vient = self.va_et_vient
		butoir = self.butoir
		remplissage_vitre = self.remplissage_vitre
		cintre = self.cintre
		triangle = self.triangle
		division = self.division
		nb_division = self.nb_division
		laque = self.laque
		moustiquaire = self.moustiquaire
		type_moustiquaire = self.type_moustiquaire
		tms = self.tms
		rec_largeur = self.largeur
		rec_hauteur = self.hauteur
		intermediaire = self.intermediaire
		rec_dimension = self.dimension
		rec_pu_ttc = self.pu_ttc
		rec_ref = self.order_ref
		rec_qty = self.quantity
		image = self.image
		order_id = self.order_id
		#rec_total = self.browse(cr, uid, ids, context=context)[0].totalcacher
		total = self.calcul()
		#### dÃ©but de formatisation de champ select_type pour evitÃ© d'afficher par ex coullissante2vtx ####
		types = select_type.name
		vitre = ''
		poignee = ''
		btr = ''
		oscillo = ''
		v_et_v = ''
		rempli = ''
		ctr =''
		lq = ''
		trgl = ''
		mstqr = ''
		dvs = ''
		tmss = ''
		simple_double=''
		deco=''
		#name = ''
		intermdr = ''
		inegalit = ''
		if type_vitre:
			if type_vitre=='double':
				simple_double=' double,'
		dec=decoratif.name
		if ((decoratif.name is not None) and(decoratif.name!=False)):
			if dec==u'Compliqué':
				deco=u' compliqué,'
		if intermediaire:
			if intermediaire == 'sans':
				intermdr = ''
		if intermediaire == 'avec':
			intermdr = u' avec intermédiaire, '
		if inegalite:
			if inegalite == 'egaux':
			 inegalit = ''
		if inegalite == u'inegaux':
			inegalit = u'inégaux,'
			if ((vitrage.name==False) or (vitrage.name is None)):
				vitre = '\n - Vitrage : standard, '
			else:
				vitre = u"\n - Vitrage : "+vitrage.name+", "
		if ((poigne.name is not None) and (poigne.name!=False)):
			poignee = u''+poigne.name+''
				
			if butoir:
				btr = " avec butoir, "
			if va_et_vient:
				v_et_v =" avec va et vient,"
			if oscillo_battant:
				oscillo = " oscillo battant, "
			if remplissage_vitre:
				if remplissage_vitre == 'standard':
					remplissage_vitre = ''
				if remplissage_vitre == u'pleine_2_3':
					remplissage_vitre = u'2/3 pleine'
				if remplissage_vitre == u'pleine_1_2':
					remplissage_vitre = u'1/2 pleine'
				if remplissage_vitre == u'pleine_1_3':
					remplissage_vitre = u'1/3 pleine'
				if remplissage_vitre == u'pleine_bardage':
					remplissage_vitre = u'Pleine/bardage'

				rempli = " "+str(remplissage_vitre)+", "
			if cintre:
				ctr = u" cintré, "
			if laque:
				lq = u" laqué, "
			if triangle:
				trgl = u" Triangle, "
			if moustiquaire:
				mstqr = "  avec moustiquaire "
			if division:
				if(nb_division>1):
					dvs = " "+str(nb_division)+" divisions, "
				else:  
					dvs = " "+str(nb_division)+" division, "
			if tms != 0.0:
				tmss = " TMS, "
		type_porte =u'Fenêtre'
		if types == 'Coulissante 2VTX':
			serrure = ''
			if tms != 0.0:
				type_porte = 'Porte'
		if serr.name is not None:
			if moustiquaire:
				serrure = u' 2 serrures encastrées 2 points ' 
			else:
				serrure = u' 1 poignee 4 points à  clef'
		else:
			if moustiquaire:
				serrure = u' 2 serrures encastrées 2 points'
			else:
				serrure = u' 1 poignee et 1 serrures encastrées 2 points'
				types = u" "+type_porte+" Coulissante 2VTX "+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" "+serrure+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
			
			if types == 'Coulissante 1VTL':
				serrure = ''
				if serr.name is not None:
					if moustiquaire:
						serrure = u' 2 serrures encastrées 2 points'
					else:
						serrure = u' 1 poignée 4 points à  clef'
				else:
					if moustiquaire:
						serrure = u' 2 serrures encastrées 2 points'
					else:
						serrure = u' 1 poignée 2 points'
				types = u"Porte Coulissante 1VTL "+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" "+serrure+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
		if types == 'Glandage':
			types = "Glandage"+"\n"
			if types == 'Coulissante 3VTX':
				serrure = ''
				if tms != 0.0:
					type_porte = 'Porte'
				if serr.name is not None:
					if moustiquaire:
						serrure = u' 2 serrures encastrées 2 points'
					else:
						serrure = u' 1 poignée 4 points à  clef et 1 serrure encastrée 2 point'
				else:
					if moustiquaire:
						serrure = u' 2 serrures encastrées 2 points'
					else:
						serrure = u' 1 poignée et 1 serrures encastrées 2 points'
				types = u" "+type_porte+" Coulissante 3VTX "+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" "+serrure+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
			if types == 'Coulissante 4VTX':
				serrure = ''
				if tms != 0.0:
					type_porte = 'Porte'
				if serr.name is not None:
					if moustiquaire:
						serrure = u' 3 serrures encastrées 2 points'
					else:
						serrure = u' 1 poignée 4 points à  clef'
				else:
					if moustiquaire:
						serrure = u' 3 serrures encastrées 2 points'
					else:
						serrure = u' 1 poignée et 2 serrures encastrées 2 points'
				types = u" "+type_porte+" Coulissante 4VTX "+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" "+serrure+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
			if types == 'Porte ouvrante 1VTL':
				types = u" Porte ouvrante 1VTL "+"\n - Accessoires :"+" ".join((tmss+" "+intermdr+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
		if types == u'Fenêtre ouvrante 1VTL':
			types = u" Fenêtre ouvrante 1VTL  "+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
			if types == 'Porte ouvrante 2VTX':
				types = u" Porte ouvrante 2VTX  "+"\n - Accessoires :"+" ".join((inegalit+" "+tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
			if types == u'Fenêtre ouvrante 2VTX':
				types = u" Fenêtre ouvrante 2VTX  "+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"            
			
		if types == 'A soufflet':
			types = u" A soufflet  "+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"      
			if types == 'Fixe':
				if type_fix:		
					if type_fix == 'imposte':
						types = "Imposte Fixe"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"            
					if type_fix == 'soubassement':
						types = "Soubassement Fixe"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"            
					if type_fix == 'lateral':
						types = u"Latéral Fixe"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"            
		else:
			types = u"Fixe"+"\n"
			if types == 'Moustiquaire':
				types = u"Moustiquaire indépendant"+"\n"
			if types == 'Naco':
				types = u"Naco"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"            
			if types == 'Poteau rectangle' or 'Poteau d\'angle' or 'Tendeur':
				
				if types == 'Poteau rectangle':
					types = "Poteau rectangle"+"\n"
				if types == 'Poteau d\'angle':
					types = "Poteau d'angle"+"\n"
					if types == "Tendeur":
						types = "Tendeur"+"\n"
						if types == 'Bardage PVC':
							types = "Bardage PVC"+"\n"
							
						if types == 'Projetant':
							types = "Projetant"+"\n"
		
		lxh=types
		if types == 'Poteau rectangle':
				 if (rec_dimension and rec_pu_ttc):
					 lxh=lxh+" \n\t - Dimension : %d x %d \n"%(rec_dimension,rec_pu_ttc,)
		else:
				if(rec_largeur and rec_hauteur):
					lxh=lxh+"- Dimension : %d x %d HT \n"%(rec_largeur,rec_hauteur,)
			#i = 0
		#product_obj = self.pool.get('product.product')
		#product_ids = product_obj.search(cr, uid, [('type','=',type)])
		#for prod in product_obj.browse(cr, uid, ids, context=context):
		
			#raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (product_ids))
		
		name = lxh

		res_image = tools.image_resize_image(image, (64, 64), 'base64', 'PNG', False)
		sale_order_line_obj.create({'product_id':select_type.id,'name': name,'order_id':order_id, 'product_uom_qty': rec_qty, 'price_subtotal' : total['totalcacher'], 'price_unit': total['totalcacher']/rec_qty,'image':res_image})
		return True
	
	####cette fonction est appellÃ©e pour mettre Ã  jour le total sur le pop-up Ã  chaque modification d'un champ sans quiter la fenÃªtre####
	@api.onchange('largeur', 'hauteur', 'dimension', 'pu_ttc', 'quantity', 'select_type', 'vitre',
			'type_vitre','decoratif', 'poigne', 'serr','nb_poigne','nb_serr','oscillo_battant',
			'va_et_vient', 'butoir','remplissage_vitre', 'cintre', 'triangle','division','nb_division', 'laque',
			'moustiquaire', 'type_moustiquaire', 'tms','intermediaire')	
	def onchange_fields(self):
		dict_total = self.calcul()
		
		self.total = dict_total['total']
		self.totalcacher = dict_total['totalcacher']
		self.cacher = dict_total['cacher']
		self.hidder_autre_option = dict_total['hidder_autre_option']
		self.image = dict_total['image']
	####cette fonction permet de faire le calcul comme dans Excel, elle est appellÃ©e dÃ¨s qu'on veut faire un calcul####
	def calcul(self):
		

		######################
		largeur = self.largeur
		hauteur = self.hauteur
		dimension = self.dimension
		pu_ttc = self.pu_ttc
		quantity = self.quantity
		select_type = self.select_type.id
		vitre = self.vitre.id
		type_vitre = self.type_vitre
		decoratif = self.decoratif.id
		poigne = self.poigne.id
		serr = self.serr.id
		nb_poigne = self.nb_poigne
		nb_serr = self.nb_serr
		oscillo_battant = self.oscillo_battant
		va_et_vient = self.va_et_vient
		butoir = self.butoir
		remplissage_vitre = self.remplissage_vitre
		cintre = self.cintre
		triangle = self.triangle
		division = self.division
		nb_division = self.nb_division
		laque = self.laque
		moustiquaire = self.moustiquaire
		type_moustiquaire = self.type_moustiquaire
		tms = self.tms
		intermediaire = self.intermediaire
		res_image = self.image
		######################
		val_total = 0.0
		val_types = 0.0
		val_vitre = 0.0
		val_type_vitre = 1
		val_autre_vitrage = 0.0
		val_decoratif = 0.0
		val_poigne = 0.0
		val_serr = 0.0
		val_serr_a_cle = 0.0
		val_oscillo_battant = 0.0
		val_va_et_vient = 0.0
		val_butoir = 0.0
		val_remplissage_vitre = 1
		val_cintre = 1
		val_triangle = 1
		val_laque = 1
		val_moustiquaire = 0.0
		val_tms = tms / 100
		cacher = False
		hidder_autre_option = False
		cacherlh = False
		types = ""

		res = {}
		
			#si le champ vitre n'es pas vide c'est Ã  dire contient une valeur . Et comme cette valeur est reliÃ©e Ã  l'objet mim.article donc 
		#on doit recupÃ©rer l'objet puis le parcourir pour obtenir l'attribut category_ids : self.pool.get('mim.article').browse(cr, uid, vitre, context=context) . Il suffit en suite de rÃ©cupÃ©rer le prix si id est vrai. Idem pour decoratif, poigne et serrure
		if vitre:
			#raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (vitre))
			categ = self.env['mim.article'].browse(vitre)
		
			val_vitre = categ.price

		if type_vitre == 'double':
			if vitre:
				val_type_vitre = 2
		else:
			val_vitre = 55000

		if decoratif:
				categ = self.env['mim.article'].browse(decoratif)
				if categ.category_ids.id:
					val_decoratif = categ.price
	
		if poigne:
				categ = self.env['mim.article'].browse(poigne)
				if categ.category_ids.id:
					val_poigne = categ.price * nb_poigne
	
		if serr:
				categ = self.env['mim.article'].browse(serr)
				if categ.category_ids.id:
					val_serr = categ.price * nb_serr

		if oscillo_battant:
			val_oscillo_battant = 150000

		if va_et_vient:
			if select_type == 'porte_ouvrante2vtx':
				val_va_et_vient = 480000
		else:
			val_va_et_vient = 240000

		if butoir:
			val_butoir = 21000

		if remplissage_vitre is not None:	
			if remplissage_vitre == 'standard':
				val_remplissage_vitre = 1
			if remplissage_vitre == 'pleine_2_3':
				val_remplissage_vitre = 1.14
			if remplissage_vitre == 'pleine_1_2':
				val_remplissage_vitre = 1.1
			if remplissage_vitre == 'pleine_1_3':
				val_remplissage_vitre = 1.07
			if remplissage_vitre == 'pleine_bardage':
				val_remplissage_vitre = 1.2
			
		if cintre:
		   val_cintre = 2
	
		if triangle:
		   val_triangle = 1.50

		if laque:
		   val_laque = 1.15
	
		if select_type:
			#raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (vitre))
			prod = self.env['product.product'].browse(select_type)
		
			types = prod.name
				

			if types == 'Coulissante 2VTX':
				#image_name='image7.png'
				if moustiquaire:
					val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
					val_total = (((((largeur*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre*val_triangle)+val_moustiquaire)*val_laque
		#raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (types))
			

		if types == 'Coulissante 1VTL':
				#image_name='image2.png'
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((((largeur*2)*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre/2)*val_laque)+val_moustiquaire

		if types == 'Coulissante 3VTX':
				#image_name='image3.png'
			if moustiquaire:
				val_moustiquaire = (((largeur/3*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((largeur*hauteur)/1000000*(180000*(1+(tms / 100))+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)+val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.025*1.08*val_cintre+val_moustiquaire)*val_laque

		if types == 'Coulissante 4VTX':
				#image_name='image4.png'
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = (((largeur*hauteur)/1000000*(180000/2*(1+(tms / 100))*val_remplissage_vitre+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*2+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.05*1.025*1.08*val_cintre*val_laque)+val_moustiquaire
			
	
		if types == 'Porte ouvrante 2VTX':
				#image_name='image5.png'
			if moustiquaire:
				val_moustiquaire = (((largeur/hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = (((largeur*hauteur)/1000000*((210222+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+92884+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre*val_laque)+val_moustiquaire

		if types == 'Porte ouvrante 1VTL':
				#image_name='image6.png'
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((largeur*hauteur)/1000000*(210000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+58652+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre+val_moustiquaire)*val_laque
		if types == u'Fenêtre ouvrante 1VTL':
				#image_name='image3.png'
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
				val_total = ((((largeur*hauteur)/1000000*(210000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+58652+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre+val_moustiquaire)*val_laque

				if types == u'Fenêtre ouvrante 2VTX':
					#image_name='image8.png'	
					if moustiquaire:
						val_moustiquaire = (((largeur/hauteur)/1000000*13500)*1.2*1.08*1.4)
				val_total = ((((largeur*hauteur)/1000000*(210222+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+92884+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir+40000)*1.15*1.08*val_cintre*val_laque)+val_moustiquaire
	
		if types == 'A soufflet':
				#image_name='image1.png'
			if division:
				val_total = (((((largeur/nb_division)*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*nb_division
			else:
				if moustiquaire:
					val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
				val_total = ((((largeur*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms/100))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*val_laque)+val_moustiquaire
		if types == 'Projetant':
				#image_name='image2.png'
			if division:
				val_total = (((((largeur/nb_division)*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*nb_division
			else:
				if moustiquaire:
						val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
				val_total = ((((largeur*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms/100))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*val_laque)+val_moustiquaire
			
		if types == 'Fixe':
				#image_name='image11.png' 	
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
			val_total = ((largeur*hauteur)/1000000*(150000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*val_remplissage_vitre*1.15*1.08*val_cintre*val_triangle*val_laque)+val_moustiquaire

		if types == 'Moustiquaire':
				#image_name='image12.png'
			cacher = True
			if type_moustiquaire == 'fixe':
				val_total = ((((largeur/nb_division)*hauteur)/1000000*13500)*1.2*1.08*1.4)*nb_division
			if type_moustiquaire == 'coulissante':
				val_total = ((((largeur/nb_division)*hauteur)/1000000*81000)*1.2*1.08)*nb_division

		if types == 'Naco':
				#image_name='image13.png'	
			if moustiquaire:
				val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
			if division:

				val_total =(((largeur/nb_division)*hauteur)/1000000*(150000+val_decoratif+val_autre_vitrage+(3000*(hauteur/100))))*1.15*1.08*val_cintre*val_laque*nb_division
			else:
		
				val_total =((((largeur*hauteur)/1000000*(150000+val_vitre*val_type_vitre+val_autre_vitrage+(3000*(hauteur/100))))*1.15*1.08*val_cintre*val_laque))+val_moustiquaire


		if types == 'Poteau rectangle':
				#image_name='image14.png'
			cacher = True
			if laque == True:
				val_total = ((dimension/1000)*pu_ttc)*val_laque
			if laque == False:
				val_total = ((dimension/1000)*pu_ttc)*1

		if types == 'Poteau d\'angle':
				#image_name='image15.png'
			cacher = True
			if laque == True:
				val_total = ((dimension/1000)*pu_ttc)*val_laque
			if laque == False:
				val_total = ((dimension/1000)*pu_ttc)*1

		if types == 'Tendeur':
				#image_name='image16.png'
			cacher = True
			if laque == True:
				val_total = ((dimension/1000)*pu_ttc)*val_laque
			if laque == False:
				val_total = ((dimension/1000)*pu_ttc)*1
			
		if types == 'Bardage PVC':
				#image_name='image17.png'
			cacher = True
			hidder_autre_option = True 
			val_total = ((largeur*hauteur)/1000000)*45000/1.2 
			##############################################Atout modification Ando#######################################################
		
		image_name = 'image0.png'
			
		if types == 'A soufflet':
			image_name='image1.png'
			if nb_division==2:
				image_name='image3.png'
				
		if types == 'Projetant':
			image_name='image2.png'
			if nb_division==2:
				image_name='image4.png'
						
		if types == u'Fenêtre ouvrante 1VTL':
			image_name='image11.png'
			if remplissage_vitre == 'pleine_bardage':
				image_name='image12.png'
				
		if types == u'Fenêtre ouvrante 2VTX': 
			image_name='image13.png'
			if remplissage_vitre:                
				if remplissage_vitre == 'pleine_bardage':
					image_name='image14.png'
		
		if types == 'Fixe':
			image_name='image17.png'
			if nb_division==2:
				image_name='image18.png'
			if nb_division==3:
				image_name='image19.png'
		#intermediaire = self.browse(cr, uid, ids, context=context)[0].intermediaire
		
		if types == 'Porte ouvrante 1VTL':
			image_name='image26.png'
			if (remplissage_vitre and remplissage_vitre!='standard') :
				if remplissage_vitre == u'pleine_bardage':
					if intermediaire == 'avec':
						image_name='image21.png'
					else : image_name='image20.png'

				if remplissage_vitre == u'pleine_2_3':
					image_name='image22.png'

				if remplissage_vitre == u'pleine_1_2':
					image_name='image23.png'

				if remplissage_vitre == u'pleine_1_3':
					image_name='image24.png'

			elif intermediaire == 'avec':
					image_name='image25.png'
					
		if types == 'Porte ouvrante 2VTX':
			image_name='image33.png'
			if (remplissage_vitre and remplissage_vitre!='standard') :
				if remplissage_vitre == u'pleine_bardage':
					if intermediaire == 'avec':
						image_name='image28.png'
					else : image_name='image27.png'
				if remplissage_vitre == u'pleine_2_3':
					image_name='image29.png'
				if remplissage_vitre == u'pleine_1_2':
					image_name='image30.png'
				if remplissage_vitre == u'pleine_1_3':
					image_name='image31.png'
			elif intermediaire == 'avec':
					image_name='image32.png'        
					
		if tms == 0.0:
			if types == 'Coulissante 2VTX':
				image_name='image34.png'
			if types == 'Coulissante 3VTX':
				image_name='image36.png'
			if types == 'Coulissante 4VTX':                
				image_name='image35.png'
		else :
			if types == 'Coulissante 1VTL': 
				image_name='image42.png'
		
		if types == 'Coulissante 2VTX':
			image_name='image43.png'
			if (remplissage_vitre and remplissage_vitre!='standard') :
				if remplissage_vitre == u'pleine_bardage':
					if intermediaire == 'avec':
						image_name='image38.png'
					else : image_name='image0.png'
				if remplissage_vitre == u'pleine_2_3':
					image_name='image0.png'
				if remplissage_vitre == u'pleine_1_2':
					image_name='image39.png'
				if remplissage_vitre == u'pleine_1_3':
					image_name='image40.png'
			elif intermediaire == 'avec':
				image_name='image41.png'
					
		if types == 'Coulissante 3VTX':
			image_name='image44.png'
		
		if types == 'Coulissante 4VTX':                
			image_name='image45.png'
				 
		img_path = modules.get_module_resource('mim_module_add_image', 'static/src/img', (image_name))
		with open(img_path, 'rb') as f:
			image = f.read()
		#res_image = tools.image_resize_image_big(image.encode('base64'))
		res_image = base64.b64encode(image)
	
		return {'total' : val_total* quantity* 1.10 ,'totalcacher' : val_total* quantity* 1.10, 'cacher' : cacher, 'hidder_autre_option': hidder_autre_option,'image': res_image}



class sale_order_line(models.Model):
	_inherit = "sale.order.line"
	image = fields.Binary('Image')


class sale_order(models.Model):
	
	_inherit = "sale.order"
	
	@api.multi
	def action_mim_wizard(self):
	  
		mod_obj = self.env['ir.model.data']
		#res = mod_obj.env.ref('mim_module.view_mim_wizard').id
		#res_id = res and res[1] or False
		ctx = dict()
		sujet = self.name
		order_ref = self.name
		order_ref = sujet[2:]
		order_id = self.id
		ctx.update({
			'default_sujet': 'Devis ' + sujet,
			'default_order_ref':order_ref,
			#ando
			'default_order_id' : order_id,
		})
		
	####permet la crÃ©ation de la nouvelle fenÃªtre pop-up###
		return {
			'name': 'Mim Wizard',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mim.wizard',
			'nodestroy': True,
			'target': 'new',
			'context': ctx,
	####
		}

	note = fields.Text('Terms and conditions',default=u'''Délais de fabrications : ... semaines après date de confirmation de commande, sous réserve de disponibilité en stock.
							Garantie : Tous les accessoires sont garantis UN an.
							Mode de paiement :
							-    50% à la commande
							-    50% avant livraison
							Service : Livraison et pose gratuites pour Antananarivo et banlieue proche. A défaut d'électricité, le carburant du groupe électrogène fourni par MIM sera à la charge du client.
							Toute modification ultérieure fera l'objet d'une réactualisation de notre offre.
							Si cette offre vous convient, merci de nous la renvoyer signée avec la mention "Bon pour accord"''')
	monnaie_lettre = fields.Char('Total en toute lettre',size =128)
	
	#Transformation du champs total chiffre en total toute lettre
	def convNombre2lettres(self, nombre):
		schu=["","UN ","DEUX ","TROIS ","QUATRE ","CINQ ","SIX ","SEPT ","HUIT ","NEUF "]
		schud=["DIX ","ONZE ","DOUZE ","TREIZE ","QUATORZE ","QUINZE ","SEIZE ","DIX SEPT ","DIX HUIT ","DIX NEUF "]
		schd=["","DIX ","VINGT ","TRENTE ","QUARANTE ","CINQUANTE ","SOIXANTE ","SOIXANTE ","QUATRE VINGT ","QUATRE VINGT "]
		s=''
		reste=nombre
		i=1000000000 
		while i>0:
			y=reste/i
			if y!=0:
				centaine=y/100
				dizaine=(y - centaine*100)/10
				unite=y-centaine*100-dizaine*10
				if centaine==1:
					s+="CENT "
				elif centaine!=0:
					s+=schu[centaine]+"CENT "
					if dizaine==0 and unite==0: s=s[:-1]+"S " 
				if dizaine not in [0,1]: s+=schd[dizaine] 
				if unite==0:
					if dizaine in [1,7,9]: s+="DIX "
					elif dizaine==8: s=s[:-1]+"S "
				elif unite==1:   
					if dizaine in [1,9]: s+="ONZE "
					elif dizaine==7: s+="ET ONZE "
					elif dizaine in [2,3,4,5,6]: s+="ET UN "
					elif dizaine in [0,8]: s+="UN "
				elif unite in [2,3,4,5,6,7,8,9]: 
					if dizaine in [1,7,9]: s+=schud[unite] 
					else: s+=schu[unite] 
				if i==1000000000:
					if y>1: s+="MILLIARDS "
					else: s+="MILLIARD "
				if i==1000000:
					if y>1: s+="MILLIONS "
					else: s+="MILLIONS "
				if i==1000:
					s+="MILLE "
			#end if y!=0
			reste -= y*i
			dix=False
			i/=1000;
		#end while
		if len(s)==0: s+="ZERO "
		#return s
		s = s.lower()
		s0 = s[0]
		s0 = s0.upper()
		s = s0 + s[1:]
		return s
	
	#Mettre le debut de la chaîne de caractère en majuscule
	def capitaliser (self, chaine):
		s = chaine.lower()
		s0 = s[0]
		s0 = s0.upper()
		s = s0 + s[1:] 
		return s
	
	#Séparer la partie decimale de la partie entière pour appliquer à chacun la fonction convNombre2lettres()
	def traitement_virgule (self, nombre):
		s=''
		lettre0 = str(nombre)
		lettre1 = lettre0.split('.')
		entiere1 = lettre1[0]
		decimal1 = lettre1[1]
		entiere2 = int(entiere1)
		decimal2 = int(decimal1)
		'''query = """select res_currency.name 
					from res_users 
					inner join (res_company  inner join res_currency on res_company.currency_id=res_currency.id)
					 on res_users.company_id=res_company.id 
					 where res_users.id={0}""".format(uid)
		cr.execute(query)
		res = cr.dictfetchone()'''
		#currency_name = self.browse(cr, uid, ids, context=context)[0].pricelist_id.currency_id.name
		
		pricelist_id = self.pricelist_id.id
		currency_name = self.env['product.pricelist'].browse(pricelist_id).currency_id.currency_name
		currency_name = self.capitaliser(currency_name)
		
		lettre_ent = self.convNombre2lettres(entiere2)
		lettre_dec = self.convNombre2lettres(decimal2)
		lettre_dec = lettre_dec.lower()
		if len(decimal1)>1:
			if decimal1[0]=='0' and decimal1[1]!='0':
				lettre_dec = 'zero ' + lettre_dec
		if decimal2 == 0 :
			lettre_dec = ''
		s = lettre_ent+" "+currency_name+" "+lettre_dec
		return {'monnaie_lettre' : s}
	
	#Redefinition de fonction button_dummy() de la classe mère sale_order
	'''def button_dummy(self, cr, uid, ids, context=None):
		chiffre = self.browse(cr, uid, ids, context=context)[0].amount_total
		value = self.traitement_virgule(cr, uid, ids,chiffre,context)
		sale_order = self.pool.get('sale.order')
		sale_order.write(cr, uid, ids,value, context)
		return True'''
	