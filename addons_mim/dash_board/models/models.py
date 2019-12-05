# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from openerp.tools.translate import _
import datetime
import calendar
import xml.etree.ElementTree as ET




class ajout(models.Model):
	''' Class Ajout:
			Ajoute un champ mois_order dans sale.order
		mois_order contient les id des mois dans monthyear
	'''
	_inherit = 'sale.order'

	mois_order = fields.Many2one(comodel_name="monthyear")
	for_total_bon_commande = fields.Integer(default=1)
	total_bon_de_commande = fields.Integer(compute='calcul_total_bon_commande', store=False, string='Total commande')

	@api.one
	def calcul_total_bon_commande(self):
		for record in self:
			total_bon = 0
			for line in record:
				total_bon += self.for_total_bon_commande
			record['total_bon_de_commande'] = total_bon


	@api.model
	def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
		res = super(ajout, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
		if 'total_bon_de_commande' in fields:
			for line in res:
				if '__domain' in line:
					lines = self.search(line['__domain'])
					total_bon = 0
					for current_account in lines:
						total_bon += current_account.for_total_bon_commande
					line['total_bon_de_commande'] = total_bon
		
		return res


class message(models.Model):
	"""docstring for message"""
	_name = 'message'

	message = fields.Text(default="Filter added to Dashboard", readonly=True)


class monthyear(models.Model):
	'''
	Class monthyear:
		classe comportant un champ name dans lequel sont stockées les mois January-December affiché dans le graph
	'''
	_name = 'monthyear'

	name = fields.Char(default='')


class menuwizard(models.TransientModel):
	'''
	Classs menuwizard:
		Classe affichant le popup
	'''
	_name = 'menuwizard'

	id_action_to_delete = fields.Integer('id action a supprimer')
	id_view_to_delete = fields.Integer('id view a supprimer')
	ajout_dashboard = fields.Boolean(default=True)

	def mois_create(self):
		'''
		La fonction mois_create insère les mois de l'années dans le champ name du modèle monthyear si il n'existe pas encore
		'''
		obj = self.env['monthyear']

		if obj.search([("id", "=", 1)]).exists():
			pass
		else:
			for i in range(1,13):
				obj.create({"name":calendar.month_name[i]})

	def supprimer_action_vue(self):
		'''
		La fonction supprimer_action_vue supprime les actions et vues créées auparavant grâce aux id to delete
		'''

		action = self.env['menuwizard'].search([('id_action_to_delete','!=',0)]).mapped('id_action_to_delete')
		view = self.env['menuwizard'].search([('id_view_to_delete','!=',0)]).mapped('id_view_to_delete')
		objet_action = self.env['ir.actions.act_window']
		objet_view = self.env['ir.ui.view']


		for act_id in action:
			browse_action = objet_action.browse(act_id)
			browse_action.unlink()


		for view_id in view:
			browse_view = objet_view.browse(view_id)
			browse_view.unlink()

	def year_only(self, liste):
		'''
		La fonction year_only reçoit en paramètre une liste de string des date_order sous forme 'Y-M-D H-m-s 'et renvoies une liste des Y
		'''
		new_list = []


		for element in liste:
			date_with_time_list = element.split(' ')
			date_only = date_with_time_list[0]
			year_month_date = date_only.split('-')
			year_only = year_month_date[0]
			if year_only not in new_list:
				new_list.append(year_only)
			else:
				pass
		return new_list

	def select(self):
		'''
		Fonction Select:
			retourne tous les années présents dans la base
		'''
		retour = []
		annee_courant = datetime.datetime.now().strftime('%Y')
		annee_debut_for_iter = int(annee_courant) - 10
		annee_fin_for_iter = int(annee_courant) + 10
		for element in range(annee_debut_for_iter, annee_fin_for_iter+1):
			retour.append((str(element),str(element)))
		'''annee = self.env['sale.order'].search([('state', '!=', 'cancel')]).mapped('date_order')
		new_year = self.year_only(annee)
		new_year.reverse()
		select_annee = []


		for date_order_tmp in new_year:
			test_select_annee_exist = (date_order_tmp,date_order_tmp)
			if test_select_annee_exist not in select_annee:
				select_annee.append(test_select_annee_exist)
			else:
				pass
		return select_annee'''
		return retour

	def select_menu(self):
		'''Return the list of menu for dashboard'''

		menu = self.env['ir.ui.view'].search([('model', '=', 'board.board'), ('type','=','form'), ('name', '!=', 'vue_wizard_sale')])
		select_menu = []
		for element in menu:
			tmp = (element.id, u'{}/{}/{}'.format(_('Reporting'), _('Dashboards'), _(element.name)))
			select_menu.append(tmp)
		return select_menu

	def generer_domain_date_order(self, debut, fin, mois_afficher, nb_jours_fin_mois):
		'''
		Fonction generer_domain_date_order:
			Génère une liste comprenant les domains pour afficher
		'''
		succession = range(int(debut),int(fin)+1)
		domain = []


		for year in succession:
			domain.append(('date_order','>=','{}-01-01'.format(year)))
			domain.append(('date_order','<=','{}-{}-{}'.format(year,mois_afficher,nb_jours_fin_mois)))
		return domain

	def operateur_with_domain(self,domain):
		'''
			Fonction operateur_with_domain:
				ajoute les opérateurs or(|) et and (&) pour transformer le domain en domain multiple
		'''
		nb_operateur = len(domain) - 1
		for i in range(nb_operateur):
			if domain[0] == '&':
				domain.insert(0,'|')
			else:
				domain.insert(0,'&')
		return domain

	def ajouter_mois(self,debut,fin):
		'''
			Fonction ajouter_mois:
				ajoute le mois en int de chaque date_order de sale.order dans le champ mois_order
		'''
		obj = self.env['sale.order'].search([('date_order', '>=', '{}-01-01'.format(debut)), ('date_order', '<=', '{}-12-31'.format(fin))])
		for element in obj:
			element_str = element.date_order.strftime('%Y-%m-%d %H-%M').split(" ")
			element_date = element_str[0]
			element_split = element_date.split('-')
			if(element.mois_order == int(element_split[1])):
				pass
			else:
				self.env["sale.order"].search([("id","=",element.id)]).write({'mois_order' : int(element_split[1])})

	mois_user = fields.Boolean(default=False)
	mois_afficher = fields.Selection([('1', 'Janvier'), ('2', u'Février'), ('3', 'Mars'), ('4', 'Avril'), ('5', 'Mai'), ('6', 'Juin'), ('7', 'Juillet'), ('8', u'Août'), ('9', 'Septembre'), ('10', 'Octobre'), ('11', 'Novembre'), ('12', u'Décembre')], default='12')
	annee_debut = fields.Selection(select, required=True)
	annee_fin = fields.Selection(select, required=True)
	nom_dashboard = fields.Selection(select_menu)
	graph = fields.Boolean(default=False)
	nom_board = fields.Char()
	choix_devis_bon_commande = fields.Selection([('devis', 'Devis'), ('bon_de_commande', 'Bon de commande')], required=True, default='bon_de_commande')
	choix_context_measures = fields.Selection([('for_total_bon_commande', 'Nombre de commande'), ('amount_total', 'Montant')])

	@api.constrains('annee_debut', 'annee_fin')
	def verification_iteration(self):
		if int(self.annee_debut) > int(self.annee_fin):
			raise  exceptions.ValidationError(u"L'année fin doit être supérieure ou égale à l'année fin")

	@api.multi
	def creation_vue(self):
		self.supprimer_action_vue()
		self.mois_create()
		#date_db = self.env['sale.order'].search([('date_order', '>=', '{}-01-01'.format(self.annee_debut)), ('date_order', '<=', '{}-12-31'.format(self.annee_fin))]).mapped('date_order')
		
		year_str = []

		for element in range(int(self.annee_debut),int(self.annee_fin)+1):
			year_str.append(str(element))

		if not self.mois_user:
			mois = datetime.datetime.now().strftime('%m')
			nb_jours_fin_mois_list = calendar.monthrange(int(self.annee_fin), int(mois))
			jours_fin = nb_jours_fin_mois_list[1]

		else :
			nb_jours_fin_mois_list = calendar.monthrange(int(self.annee_fin), int(self.mois_afficher))
			jours_fin = nb_jours_fin_mois_list[1]
			mois = self.mois_afficher

		#year_str = self.year_only(date_db)
		view_inherit = self.env['ir.ui.view'].search([('id','=',self.nom_dashboard)])
		action_suite=''
		etat = []

		if self.choix_devis_bon_commande == 'devis':
			etat =	[('state', 'in', ['draft', 'sent'])]

		elif self.choix_devis_bon_commande == 'bon_de_commande':
			etat =	[('state', 'not in', ['draft', 'sent', 'cancel'])]

		if self.choix_context_measures == 'for_total_bon_commande':
			context_measures = '{"group_by": ["mois_order", "date_order:year"], "graph_measure": ["for_total_bon_commande"]}'

		elif self.choix_context_measures == 'amount_total':
			context_measures = '{"group_by": ["mois_order", "date_order:year"], "graph_measure": ["amount_total"]}'

		if self.env['ir.ui.view.custom'].search_count([('ref_id','=',view_inherit.id)])>0:
			in_view_custom = self.env['ir.ui.view.custom'].search([('ref_id','=',view_inherit.id)], order='id desc')[0]
			text_arch = ET.fromstring(in_view_custom.arch, parser=None)
			count = 0

			for text_arch in text_arch.iter('action'):

				if (('context' in text_arch.attrib) and ('domain' in text_arch.attrib)):
					domain_replace_lower = (text_arch.attrib['domain']).replace('<', '&lt;')
					domain_replace_greater = domain_replace_lower.replace('>', '&gt;')
					domain_replaced = domain_replace_greater
					action_suite_tmp = '<action context="{}" domain="{}" string="{}" name="{}" colspan="2" view_mode="{}"/> '.format(text_arch.attrib['context'], domain_replaced, text_arch.attrib['string'], text_arch.attrib['name'], text_arch.attrib['view_mode'])

				else:
					action_suite_tmp = '<action string="{}" name="{}" colspan="2" view_mode="{}"/> '.format(text_arch.attrib['string'], text_arch.attrib['name'], text_arch.attrib['view_mode'])
				action_suite = action_suite + action_suite_tmp
				count = count + 1

		if self.graph:
			self.ajouter_mois(self.annee_debut,self.annee_fin)
			domaine = self.generer_domain_date_order(self.annee_debut,self.annee_fin,mois,jours_fin)
			domaine = self.operateur_with_domain(domaine)
			domaine.insert(0, '&')
			identifiant_cursor = self.env['ir.actions.act_window'].create({
				'name':'Commande {} à {} '.format(self.annee_debut, self.annee_fin),
				'res_model':'sale.order',
				'view_type':'form',
				'view_mode':'tree,form,graph',
				'context':context_measures,
				'domain':domaine + etat
				})

			if self.ajout_dashboard:
				action = '<action string="{}" name="{}" colspan="2" view_mode="graph"/> '.format(self.nom_board, identifiant_cursor.id)
				action = action + action_suite

				view = self.env['ir.ui.view.custom'].create({
					'user_id':self.env.uid,
					'ref_id':view_inherit.id,
					'arch':'<form string="My Dashboard" create="false" delete="false" edit="false" js_class="board">\
					<board style="2-1">\
						<column>\
						%s\
					 </column>\
					</board>\
					</form>'%(action)
					})


				return {
					'name': 'Dashboard message form',
					'type': 'ir.actions.act_window',
					'res_model': 'message',
					'view_mode': 'form',
					'view_type': 'form',
					'target': 'new'
					}

			else:
				'''retour affichage normale sans ajout dashboard'''
				action = '<action string="Commande {} à {} " name="{}" colspan="2" view_mode="graph"/> '.format(self.annee_debut, self.annee_fin, identifiant_cursor.id)

				view = self.env['ir.ui.view'].create({
					'name': 'vue_wizard_sale',
					'model': 'board.board',
					'type' : 'form',
					'arch':'<?xml version="1.0"?>\
							<form string="My Dashboard" create="false" delete="false" edit="false" js_class="board">\
								<hpaned>\
									<child1>\
										%s\
									</child1>\
								</hpaned>\
							</form>'%(action)
					})

				self.env['menuwizard'].create({'annee_debut':self.annee_debut, 'annee_fin':self.annee_fin, 'id_view_to_delete':view.id, 'id_action_to_delete':identifiant_cursor.id})
				return {
				'name':_('Dashboard purchase order before %s ')%calendar.month_name[int(mois)],
				'view_mode':'form',
				'view_type':'list',
				'res_model':'board.board',
				'type':'ir.actions.act_window',
				'view_id':view.id,
				'target':'new',
				}

		else:
			identifiant = []
			liste_annee = []
			action_id_to_delete = []
			action = ''

			for year in year_str:
				if year not in liste_annee:
					identifiant_cursor = self.env['ir.actions.act_window'].create({
						'name':'Commande {}'.format(year),
						'res_model':'sale.order',
						'view_type':'form',
						'view_mode':'tree,form,graph,search',
						'context':'{"group_by":"date_order"}',
						'domain':[('date_order','>=','{}-01-01'.format(year)), ('date_order','<=','{}-{}-{}'.format(year, mois, jours_fin)), etat[0]]
						})
					action_id_to_delete.append(identifiant_cursor.id)
					#self.env['menuwizard'].create({'annee_debut':self.annee_debut,'annee_fin':self.annee_fin,'id_action_to_delete':identifiant_cursor.id})
					liste_annee.append(year)
					identifiant.append(identifiant_cursor.id)
				else :
					pass
			tmp = -1

			if self.ajout_dashboard:
				for i in range(1, len(identifiant) + 1):
					#action = action+'<action string="{} ({})" name="{}" colspan="2" view_mode="tree"/> '.format(self.nom_board,liste_annee[tmp],identifiant[-i])
					action = action + '<action string="{} ({})" name="{}" colspan="2" view_mode="list"/> '.format(self.nom_board, liste_annee[tmp], identifiant[-i])
					#context="{"group_by":"sale.order.date_order"}"
					tmp = tmp -1

				action = action + action_suite

				view = self.env['ir.ui.view.custom'].create({
					'user_id':self.env.uid,
					'ref_id':view_inherit.id,
					'arch':'<form string="My Dashboard" create="false" delete="false" edit="false" js_class="board">\
					<board style="2-1">\
						<column>\
						%s\
					 </column>\
					</board>\
					</form>'%(action)
					})



				return {
					'name': 'Dashboard message form',
					'type': 'ir.actions.act_window',
					'res_model': 'message',
					'view_mode': 'form',
					'view_type': 'form',
					'target': 'new'
					}


			else:
				'''Retour vue normale sans ajout dashboard'''
				for i in range(1, len(identifiant) + 1):
					action = action + '<action string="Commande {}" name="{}" colspan="2"/> '.format(liste_annee[tmp], identifiant[-i])
					#context="{"group_by":"sale.order.date_order"}"
					tmp = tmp -1

				view = self.env['ir.ui.view'].create({
					'name': 'vue_wizard_sale',
					'model': 'board.board',
					'type' : 'form',
					'arch':'<?xml version="1.0"?>\
							<form string="My Dashboard" create="false" delete="false" edit="false" js_class="board">\
								<hpaned>\
									<child1>\
										%s\
									</child1>\
								</hpaned>\
							</form>'%(action)
					})

				for element in action_id_to_delete:
					self.env['menuwizard'].create({'annee_debut':self.annee_debut, 'annee_fin':self.annee_fin, 'id_action_to_delete':element})

				self.env['menuwizard'].create({'annee_debut':self.annee_debut, 'annee_fin':self.annee_fin, 'id_view_to_delete':view.id})

				return {
				'name':'Dashboard purchase order before {}'.format(calendar.month_name[int(mois)]),
				'view_mode':'form',
				'view_type':'form',
				'res_model':'board.board',
				'type':'ir.actions.act_window',
				'view_id':view.id,
				'target':'new',
				'auto_refresh':True,
				}