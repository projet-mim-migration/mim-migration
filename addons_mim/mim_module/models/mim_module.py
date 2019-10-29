# Written by Lido on  Licence GPL #
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp



class article_categorie(models.Model):
	""" Class Categorie d'article """
	_name = "article.categorie"
	_description = "Categorie d'article"
	
	name = fields.Char('Catégorie', size=64, required=True)
	
	_sql_constraints = [
		('name', 'unique(name)', 'The name of the category must be unique')
	]
	_order = 'name asc'




class mim_article(models.Model):
	""" Class pour la gestion des article (nom et prix)"""
	_name = 'mim.article'
		
	name = fields.Char('Article', size=64, required=True)
	price = fields.Float('Prix', required=True)
	category_ids = fields.Many2one('article.categorie', string='Catégorie', required=True)
	
	_sql_constraints = [
		('name', 'unique(name)', 'The name of the idea must be unique')
	]

	_order = 'name asc'




class mim_wizard(models.TransientModel):
	"""  """
	_name = 'mim.wizard'
	order_ref = fields.Integer('Order Reference')    #la rÃ©fÃ©rence d'un devis
	
	sujet= fields.Char('Sujet', readonly=True)
	#'select_type':fields.selection([('coulissante2vtx','Coullissante 2 VTX'),('coulissante1vtl','Coulissante 1VTL'),('glandage','Glandage'),('coulissante3vtx','Coulissante 3VTX'),('coulissante4vtx','Coulissante 4VTX'),('porte_ouvrante1vtl',u'Porte Ouvrante 1VTL'),('fenetre_ouvrante1vtl',u'FenÃªtre Ouvrante 1VTL'),('porte_ouvrante2vtx','Porte Ouvrante  2VTX'),('fenetre_ouvrante2vtx',u'FenÃªtre Ouvrante  2VTX'),('asouflet','A Soufflet'),('projetant','Projetant'),('fixe','Fixe'),('moustiquaire_independant',u'Moustiquaire IndÃ©pendant'),('naco','Naco'),('poteau_rect_angle','Poteau Rectangle/ Angle/ Tendeur'),('bardage_pvc','Bardage PVC')], string="Type", required=True),#les diffÃ©rents types de l'article
	select_type = fields.Many2one('product.product', 'Type', domain=[('categ_id','=',3)], change_default=True)
	 #,domain=[('categ_id','=','Types')]
	
	####les diffÃ©rent propriÃ©tÃ©s####
	largeur = fields.Float('Largeur',default = 1.0)
	hauteur = fields.Float('Hauteur',default = 1.0)
	dimension = fields.Float('Dimension',default= 0.0)
	pu_ttc = fields.Float('PU TTC',default= 0.0)
	quantity = fields.Integer('Quantité')
	vitre = fields.Many2one('mim.article', string='Vitre', domain=[('category_ids', '=', 'Vitrage')])
	type_vitre = fields.Selection([('simple','Simple'),('double','Double')], string="")
	decoratif = fields.Many2one('mim.article', string='Décoratif', domain=[('category_ids', '=', 'Decoratif')])
	poigne = fields.Many2one('mim.article', string='Poignée', domain=[('category_ids', '=', 'Poignee')])
	nb_poigne = fields.Integer('Nombre',default=1)
	serr = fields.Many2one('mim.article', string='Serrure', domain=[('category_ids', '=', 'Serrure')])
	nb_serr = fields.Integer('Nombre',default=1)
	oscillo_battant = fields.Boolean('Oscillo-battant')
	va_et_vient = fields.Boolean('Va et vient')
	butoir = fields.Boolean('Butoir')
	remplissage_vitre = fields.Selection([('standard','Standard'),('pleine_2_3','2/3 pleine'),('pleine_1_2','1/2 pleine'),('pleine_1_3','1/3 pleine'),('pleine_bardage','Pleine/bardage')], string="Remplissage vitre")
	type_fixe = fields.Selection([('imposte','Imposte'),('soubassement','Soubassement'),('lateral',u'Latéral')], string="Type Fixe")
	inegalite = fields.Selection([('egaux','Egaux'),('inegaux',u'Inégaux')], string=u"Inégalité")
	type_poteau = fields.Selection([('poteau_rect','Poteau rectangle'),('poteau_angle','Poteau d\'angle'),('tendeur','Tendeur'),], string="Poteau Rect / Angle / Tendeur")
	cintre = fields.Boolean('Cintré')
	triangle = fields.Boolean('Triangle')
	division = fields.Boolean('Division')
	nb_division = fields.Integer('Nombre division',default=1)
	laque = fields.Boolean('Laqué')
	moustiquaire = fields.Boolean('Moustiquaire')
	tms = fields.Float('TMS',default= 0.0)
	type_moustiquaire = fields.Selection([('fixe','Fixe'),('coulissante','Coulissante')], string="Type de moustiquaire")
	total = fields.Float('Total', readonly=True, digits= dp.get_precision('Account'))
		####fin des diffÃ©rents propriÃ©tÃ©s####
	totalcacher = fields.Float('Total')#est utilisÃ© pour cacher/afficher le field totalcacher 
	hidder_autre_option = fields.Boolean('Cacher les autres options')#est utilisÃ© pour cacher/afficher le group Autres option dans mim_module_view.xml
	cacher = fields.Boolean('Cacher',default=False)
	intermediaire = fields.Selection([('sans',u'Sans intermédiaire'),('avec',u'Avec intermédiaire')], string=u"Intermédiaire")
	
	

	####cette fonction permet la crÃ©ation d'une ligne de commande grÃ¢ce Ã  sale_order_line_obj.create(cr, uid, {'name': name,'order_id':rec_ref, 'price_unit' : rec_total})####
	@api.multi
	def order_line_create(self):
		
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
		#rec_total = self.browse()[0].totalcacher
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
				types = "Glandage"
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
			types = u"Fixe"
			if types == 'Moustiquaire':
				types = u"Moustiquaire indépendant"
			if types == 'Naco':
				types = u"Naco"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"            
			if types == 'Poteau rectangle' or 'Poteau d\'angle' or 'Tendeur':
				if types == 'Poteau rectangle':
					types = "Poteau rectangle"
				if types == 'Poteau d\'angle':
					types = "Poteau d'angle"
				if types == "Tendeur":
					types = "Tendeur"
			if types == 'Bardage PVC':
				types = "Bardage PVC"
		
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
		sale_order_line_obj.create({
			'product_id':select_type.id,
			'name': name,
			'order_id':rec_ref, 
			'product_uom_qty': rec_qty,
			'price_subtotal' : total['totalcacher'], 
			'price_unit': total['totalcacher']/rec_qty
			})#'price_unit': total['totalcacher']/rec_qty
		
		return True
	
	####cette fonction est appellÃ©e pour mettre Ã  jour le total sur le pop-up Ã  chaque modification d'un champ sans quiter la fenÃªtre####
	@api.onchange('largeur', 'hauteur', 'dimension', 'pu_ttc', 'quantity', 'select_type', 'vitre',
			'type_vitre','decoratif', 'poigne', 'serr','nb_poigne','nb_serr','oscillo_battant',
			'va_et_vient', 'butoir','remplissage_vitre', 'cintre', 'triangle','division','nb_division', 'laque',
			'moustiquaire', 'type_moustiquaire', 'tms')
	def onchange_fields(self):
		dict_total = self.calcul()
		
		#return {'total' : val_total* quantity ,'totalcacher' : val_total* quantity, 'cacher' : cacher, 'hidder_autre_option': hidder_autre_option}
		
		self.total = dict_total['total']
		self.totalcacher = dict_total['totalcacher']
		self.cacher = dict_total['cacher']
		self.hidder_autre_option = dict_total['hidder_autre_option']
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
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = (((((largeur*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre*val_triangle)+val_moustiquaire)*val_laque
		#raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (types))
			

		if types == 'Coulissante 1VTL':
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((((largeur*2)*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre/2)*val_laque)+val_moustiquaire

		if types == 'Coulissante 3VTX':
			if moustiquaire:
				val_moustiquaire = (((largeur/3*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((largeur*hauteur)/1000000*(180000*(1+(tms / 100))+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)+val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.025*1.08*val_cintre+val_moustiquaire)*val_laque

		if types == 'Coulissante 4VTX':
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = (((largeur*hauteur)/1000000*(180000/2*(1+(tms / 100))*val_remplissage_vitre+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*2+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.05*1.025*1.08*val_cintre*val_laque)+val_moustiquaire
			
	
		if types == 'Porte ouvrante 2VTX':
			if moustiquaire:
				val_moustiquaire = (((largeur/hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = (((largeur*hauteur)/1000000*((210222+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+92884+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre*val_laque)+val_moustiquaire

		if types == 'Porte ouvrante 1VTL':
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((largeur*hauteur)/1000000*(210000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+58652+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre+val_moustiquaire)*val_laque
		if types == u'Fenêtre ouvrante 1VTL':
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((largeur*hauteur)/1000000*(210000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+58652+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre+val_moustiquaire)*val_laque

		if types == u'Fenêtre ouvrante 2VTX':   
			if moustiquaire:
				val_moustiquaire = (((largeur/hauteur)/1000000*13500)*1.2*1.08*1.4)
		val_total = ((((largeur*hauteur)/1000000*(210222+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+92884+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir+40000)*1.15*1.08*val_cintre*val_laque)+val_moustiquaire
	
		if types == 'A soufflet':
			if division:
				val_total = (((((largeur/nb_division)*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*nb_division
			else:
				if moustiquaire:
					val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
				val_total = ((((largeur*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms/100))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*val_laque)+val_moustiquaire
		if types == 'Projetant':
			if division:
				val_total = (((((largeur/nb_division)*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*nb_division
			else:
				if moustiquaire:
					val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
				val_total = ((((largeur*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms/100))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*val_laque)+val_moustiquaire
			
		if types == 'Fixe': 
			if moustiquaire:
				val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
			val_total = ((largeur*hauteur)/1000000*(150000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*val_remplissage_vitre*1.15*1.08*val_cintre*val_triangle*val_laque)+val_moustiquaire

		if types == 'Moustiquaire':
			cacher = True
			if type_moustiquaire == 'fixe':
				val_total = ((((largeur/nb_division)*hauteur)/1000000*13500)*1.2*1.08*1.4)*nb_division
			if type_moustiquaire == 'coulissante':
				val_total = ((((largeur/nb_division)*hauteur)/1000000*81000)*1.2*1.08)*nb_division

		if types == 'Naco':
			if moustiquaire:
				val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
			if division:

				val_total =(((largeur/nb_division)*hauteur)/1000000*(150000+val_decoratif+val_autre_vitrage+(3000*(hauteur/100))))*1.15*1.08*val_cintre*val_laque*nb_division
			else:
		
				val_total =((((largeur*hauteur)/1000000*(150000+val_vitre*val_type_vitre+val_autre_vitrage+(3000*(hauteur/100))))*1.15*1.08*val_cintre*val_laque))+val_moustiquaire


		if types == 'Poteau rectangle':
			cacher = True
			if laque == True:
				val_total = ((dimension/1000)*pu_ttc)*val_laque
			if laque == False:
				val_total = ((dimension/1000)*pu_ttc)*1

		if types == 'Poteau d\'angle':
			cacher = True
			if laque == True:
				val_total = ((dimension/1000)*pu_ttc)*val_laque
			if laque == False:
				val_total = ((dimension/1000)*pu_ttc)*1

		if types == 'Tendeur':
			cacher = True
			if laque == True:
				val_total = ((dimension/1000)*pu_ttc)*val_laque
			if laque == False:
				val_total = ((dimension/1000)*pu_ttc)*1
			
		if types == 'Bardage PVC':
			cacher = True
			hidder_autre_option = True 
			val_total = ((largeur*hauteur)/1000000)*45000/1.2 
	
		return {'total' : val_total* quantity ,'totalcacher' : val_total* quantity, 'cacher' : cacher, 'hidder_autre_option': hidder_autre_option}



class sale_order(models.Model):
	####override de la classe sale_order du module sale pour l'hÃ©ritage####
	_inherit = "sale.order"
	entete = fields.Text('Sujet')
	
	####cette fonction permet de rÃ©cupÃ©rer la rÃ©fÃ©rence du devis en cours de modification par ex SO003####
	@api.multi
	def action_mim_wizard(self):
	  
		mod_obj = self.env['ir.model.data']
		#res = mod_obj.env.ref('mim_module.view_mim_wizard').id
		#res_id = res and res[1] or False
		ctx = dict()
		sujet = self.name
		order_ref = self.name
		order_ref = sujet[2:]
		ctx.update({
			'default_sujet': 'Devis ' + sujet,
			'default_order_ref':order_ref,
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


