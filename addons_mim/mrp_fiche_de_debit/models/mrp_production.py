# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions



class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
        
    @api.depends('partner_id')
    def _get_partner_name(self):
        for production in self:
            production.partner_name = production.partner_id.name
    
    largeur = fields.Float(
        'Largeur'
    )
    hauteur = fields.Float(
        'Hauteur'
    )
    nbr_barre = fields.Float(
        'Nombre total de barres',
        default=0.0
    )
    product_lines1 = fields.One2many(
        'stock.move.component.line', 
        'production_id', 
        'Articles'
    )
    product_lines2 = fields.One2many(
        'stock.move.accessory.line', 
        'production_id',
        'Accessoires'
    )
    is_printable = fields.Boolean(
        'Fiche de débit standard',
        default=False
    )
    dimension = fields.Float(
        'Dimension'
    )
    vitre = fields.Many2one(
        'mim.article', 
        string='Vitre'
    )
    type_vitre = fields.Selection(
        [('simple','Simple'),
         ('double','Double')], 
        string=""
    )
    decoratif = fields.Many2one(
        'mim.article', 
        string='Décoratif'
    )
    poigne = fields.Many2one(
        'mim.article', 
        string='Poignée'
    )
    nb_poigne = fields.Integer(
        'Nombre'
    )
    serr = fields.Many2one(
        'mim.article', 
        string='Serrure'
    )
    nb_serr = fields.Integer(
        'Nombre'
    )
    oscillo_battant = fields.Boolean(
        'Oscillo-battant'
    )
    va_et_vient = fields.Boolean(
        'Va et vient'
    )
    butoir = fields.Boolean(
        'Butoir'
    )
    remplissage_vitre = fields.Selection(
        [('standard','Standard'),
         ('pleine_2_3','2/3 pleine'),
         ('pleine_1_2','1/2 pleine'),
         ('pleine_1_3','1/3 pleine'),
         ('pleine_bardage','Pleine/bardage')], 
         string="Remplissage vitre"
    )
    type_fixe = fields.Selection(
        [('imposte','Imposte'),
         ('soubassement','Soubassement'),
         ('lateral','Latéral')], 
         string="Type Fixe"
    )
    inegalite = fields.Selection(
        [('egaux','Egaux'),
         ('inegaux',u'Inégaux')], 
         string="Inégalité"
    )        
    cintre = fields.Boolean(
        'Cintré'
    )
    triangle = fields.Boolean(
        'Triangle'
    )
    division = fields.Boolean(
        'Division'
    )
    nb_division = fields.Integer(
        'Nombre division',
        default=1.0
    )
    laque = fields.Boolean(
        'Laqué'
    )
    moustiquaire = fields.Boolean(
        'Moustiquaire'
    )
    tms = fields.Float(
        'TMS'
    )
    type_moustiquaire = fields.Selection(
        [('fixe','Fixe'),
         ('coulissante','Coulissante')], 
         string="Type de moustiquaire"
    )
    intermediaire = fields.Selection(
        [('sans',u'Sans intermédiaire'),
        ('avec',u'Avec intermédiaire')], 
        string=u"Intermédiaire"
    )
    type_intermediaire = fields.Selection(
        [('vert','Vertical'),
         ('horiz','Horizontal')], 
        string=u"Type intermédiaire"
    )
    is_calculated = fields.Boolean(
        'Fiche de débit calculée',
        default=False
    )
    longueur_barre = fields.Float(
        'Longueur barre / unité ',
        required=True,
        default=5800.0
    )
    description = fields.Char(
        'Description'
    )
    partner_id = fields.Many2one(
        'res.partner', 
        'Client'
    )        
    style = fields.Selection(
        [('fr','A la française'),
         ('en','A l\'anglaise')], 
        string="Style",
        default="fr"
    )
    batis_id = fields.Many2one(
        'mim.article', 
        string='Bâtis', 
        domain=[('category_ids', '=', 'Bâtis')],
    )       
    state = fields.Selection([
         ('draft', 'New'), 
         ('verified', 'Fiche vérifiée'),
         ('validated', 'Fiche de débit validée'), 
         ('confirmed', 'Awaiting Raw Materials'),
         ('planned', 'Planned'),
         ('ready', 'Prêt à produire'),
         ('progress', 'In Progress'),
         ('done', 'Done'),
         ('cancel', 'Cancelled')], 
        string='State',
        default='draft',
        copy=False,
        track_visibility='onchange'
    )
    product_uom_id = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        oldname='product_uom', readonly=True, required=True,
        states={'draft': [('readonly', False)]})


    # 'state': fields.selection(
    #         [('draft', 'New'), 
    #         :::::::
    #         ('cancel', 'Cancelled'), 
    #         ('confirmed', 'Awaiting Raw Materials'),
    #         ('ready', 'Ready to Produce'), 
    #         ('in_production', 'Production Started'), 
    #         ('done', 'Done')],
    


    # state = fields.Selection(
    #     [('draft', 'New'), 
    #      ('verified', 'Fiche vérifiée'),
    #      ('validated', 'Fiche de débit validée'), 
    #      ('cancel', 'Cancelled'), 
    #      ('picking_except', 'Picking Exception'), 
    #      ('confirmed', 'Awaiting Raw Materials'),
    #      ('ready', 'Ready to Produce'), 
    #      ('in_production', 'Production Started'), 
    #      ('done', 'Done')],
    #     string='Status', 
    #     readonly=True,
    #     default='draft',
    #     track_visibility='onchange',
    #     help="When the production order is created the status is set to 'Draft'.\n\
    #             If the order is confirmed the status is set to 'Waiting Goods'.\n\
    #             If any exceptions are there, the status is set to 'Picking Exception'.\n\
    #             If the stock is available then the status is set to 'Ready to Produce'.\n\
    #             When the production gets started then the status is set to 'In Production'.\n\
    #             When the production is over, the status is set to 'Done'."
    # )
    # #date plannifie modifiable dans tous les etats sauf dans Termine
    date_planned_start = fields.Datetime(
        'Scheduled Date', 
        required=True, 
        select=1, 
        readonly=False, 
        states={'done':[('readonly',True)]}
    )
    
    # #permettre dediter les lignes des articles prevus
    # # product_lines = fields.One2many(
    # #     'mrp.production.product.line', 
    # #     'production_id', 
    # #     'Scheduled goods',
    # #     readonly=True, 
    # #     states={'draft':[('readonly',False)]}
    # # )
    
    # #champ permettant de prendre le nom du client
    partner_name = fields.Char(
        string='Nom du client',
        compute=_get_partner_name
    )
    
    ###########
    # PROBLEM #
    ###########


    # Redéfintion de la fonction action_produce() pour mettre stock.move à l'etat disponible        
    @api.model
    def action_produce(self, production_id, production_qty, production_mode, wiz=False):
        if production_mode == 'consume_produce':
            self.env['mrp.production'].set_move_available(production_id)
        elif production_mode == 'consume':
            for production in self.browse(production_id):
                if production.move_prod_id.id:
                    self.env['stock.move'].browse(production.move_prod_id.id).write({
                        'state' : 'flowsheeting'
                    })
                else:
                    raise exceptions.UserError(('Erreur'), (u'Cet ordre de fabrication n\'est liée à aucun mouvement de stock (stock.move)'))
        return super(MrpProduction, self).action_produce(production_id, production_qty, production_mode, wiz=wiz)
    

    # Function to calculate the necessary material 
    ##############################################

    def round_float(self, qty):
        s = str(qty)
        t = s.split('.')
        dec = 0
        if int(t[1]) > 0:
            dec = 1
        res = int(t[0]) + dec
        return res
    
    #Fonction permettant de calculer le nombre de barres en fonction de la quatité en mm de barres  
    @api.multi
    def get_nbr_barres(self, qty_mm):
        self.ensure_one()
        len_barre = self.longueur_barre
        # len_barre est la longueur d'une barre en mm par unité
        qty_barres = qty_mm / len_barre
        return self.round_float(qty_barres)
    

    # @api.multi
    # def _action_compute_lines(self, properties=None):
    #     # Compute product_lines and workcenter_lines from BoM structure
    #     #@return: product_lines
        

    #     if properties is None:
    #         properties = []
    #     results = []
    #     prod_line_obj = self.env['mrp.production.product.line']
    #     workcenter_line_obj = self.env['mrp.production.workcenter.line']
        
    #     #Modification ando
    #     prod_line_obj1 = self.env['mrp.production.product.component.line']
    #     prod_line_obj2 = self.env['mrp.production.product.accessory.line']
    #     #prod_line_obj3 = self.pool.get('mrp.production.product.all.component.line')
        
    #     for production in self:
    #         #unlink product_lines
    #         prod_line_obj.sudo().unlink([line.id for line in production.product_lines])
            
            
    #         #ando unlink product_lines1 components
    #         prod_line_obj1.sudo().unlink([line.id for line in production.product_lines1])
            
    #         #unlink product_lines2 accessories
    #         prod_line_obj2.sudo().unlink([line.id for line in production.product_lines2])
    #         #########################
            
            
    #         #unlink workcenter_lines
    #         workcenter_line_obj.sudo().unlink([line.id for line in production.workcenter_lines])
            
    #         res = self._prepare_lines(production, properties=properties)
    #         results = res[0] # product_lines
    #         results2 = res[1] # workcenter_lines
            
    #         #ando Calcul dynamique de la quatité des composants
    #         product = self.browse()[0]
    #         parent_id = product.product_id.id
    #         qty = product.product_qty
    #         largeur = product.largeur
    #         hauteur = product.hauteur
    #         tms = product.tms
    #         localdict = {}
    #         localdict['largeur'] = largeur
    #         localdict['hauteur'] = hauteur
    #         localdict['tms'] = tms
    #         localdict['result'] = None
    #         localdict['style'] = product.style
    #         localdict['vitre'] = product.remplissage_vitre
            
    #         #Mise à jour
    #         if not product.vitre :
    #             localdict['type_vitre'] = 0
    #         else:localdict['type_vitre'] = product.vitre.id
            
    #         localdict['inter'] = product.intermediaire
    #         localdict['moust'] = product.moustiquaire
            
    #         localdict['div'] = product.division
            
    #         if not product.nb_division :
    #             localdict['nb_div'] = 1.0
    #         else:localdict['nb_div'] = product.nb_division
            
    #         if not product.type_intermediaire or product.type_intermediaire=='vert':
    #             localdict['type_inter'] = 'vert'
    #         else:localdict['type_inter'] = 'horiz'
            
    #         localdict['batis'] = product.batis_id.name
            
    #         component = self.env['mrp.component']
    #         #all_component = []
    #         l = {}
    #         for line in results:
    #             line_id = line['line_id']
    #             list_id = component.search([('line_id','=',line_id)])
    #             if list_id:
    #                 for c in component.browse():
    #                     total1 = 0.0
    #                     total2 = 0.0
                        
    #                     len_total0 = 0.0
    #                     len_unit0 =0.0
    #                     qty_total0 = 0.0
    #                     #Insértion de tous les sous-composants pour l'impression
    #                     for s in c.sub_component_ids:
    #                         localdict['Q'] = qty
                            
    #                         safe_eval(s.python_product_qty, localdict, mode='exec', nocopy=True)
    #                         product_qty = float(localdict['result'])
    #                         ##################################
    #                         l['production_id'] = production.id
    #                         l['product_qty'] = product_qty
                            
    #                         localdict['QU'] = product_qty
                            
    #                         product_qty0 = product_qty
                            
    #                         safe_eval(s.python_product_qty_total, localdict, mode='exec', nocopy=True)
    #                         product_qty_total = float(localdict['result'])
                            
    #                         l['product_qty_total'] = product_qty_total
    #                         #l['product_qty_total'] = qty * l['product_qty']
                            
    #                         qty_total0 = product_qty_total
                            
    #                         localdict['QT'] = l['product_qty_total']
                            
    #                         total2 = total2 + l['product_qty_total']
    #                         if not line['is_accessory']:
    #                             l['ref'] = c.product_parent_id.ref
    #                             l['name'] = s.name
    #                             safe_eval(s.python_len_unit, localdict, mode='exec', nocopy=True)
    #                             len_unit = float(localdict['result'])
    #                             l['len_unit'] = len_unit
                                
    #                             localdict['LU'] = l['len_unit']
                                
    #                             #l['len_total'] = l['len_unit'] * l['product_qty_total']
                                
    #                             safe_eval(s.python_len_total, localdict, mode='exec', nocopy=True)
    #                             len_total = float(localdict['result'])
                                
    #                             l['len_total'] = len_total
                                
    #                             len_total0 = len_total
                                
    #                             total1 = total1 + l['len_total']
                                
    #                             LU = l['len_unit']
    #                             LT = l['len_total']
                                
    #                             len_unit0 = l['len_unit']
                                
    #                             if l['len_total']!=0.0:
    #                                 prod_line_obj1.create(l.copy())
    #                         else:
    #                             if l['product_qty_total']!=0.0:
    #                                 l['ref'] = c.product_parent_id.name
    #                                 l['name'] = s.name
    #                                 prod_line_obj2.create(l.copy())
    #                         l = {}
                            
    #                     if not line['is_accessory']:
    #                         uom = c.product_parent_id.uom_id.name
    #                         ref = c.product_parent_id.ref
    #                         len_barre = self.browse()[0].longueur_barre
                            
    #                         if uom == 'Barre':
                                
    #                             if ref !='P50-MB':
    #                                 line['product_qty'] = self.get_nbr_barres(total1)
    #                             else:
    #                                 var = (LU/100.0)*LT*qty_total0/len_barre
    #                                 line['product_qty'] = self.round_float(var)
                            
    #                         else:
    #                             line['product_qty'] = (LU * LT * product_qty_total)/10000.0
                            
    #                     else: line['product_qty'] = total2
    #                     ##########################################
                        
    #         #for move_lines in production.move_lines:
    #         # reset product_lines in production order    
    #         for line in results:
    #             if line['product_qty'] !=0.0:
    #                 line['production_id'] = production.id
    #                 prod_line_obj.create(line)  
                                
    #         #reset workcenter_lines in production order
    #         for line in results2:
    #             line['production_id'] = production.id
    #             workcenter_line_obj.create(line)
                
    #         prod_obj = self.env['mrp.production']
    #         prod_obj.write({'is_calculated':True}) 
            
    #     return results
    
    # @api.model
    # def set_move_available(self, production_id):
    #     #Rendre disponible la stock_move lié à l'ordre de fabrication
    #     production = self.browse(production_id)
    #     wf_service = netsvc.LocalService("workflow")
    #     move_obj = self.env['stock.move']
    #     if production.move_prod_id.id:
    #         #===================================================================
    #         # #creation du mouvement de l'emplacement inventaire vers WH/STOCK, mise à jour inventaire
    #         # move_obj.modifier_inventaire(cr, uid, [production.move_prod_id.id], context=context)
    #         #===================================================================
    #         wf_service.trg_validate('stock.move', production.move_prod_id.id, 'force_assign')
    #     else:
    #         raise exceptions.UserError(('Erreur'), (u'Cette ordre de fabrication n\'est liée à aucun mouvement de stock (stock.move)'))
    #     return True
    
       

       

    # @api.multi
    # def sheet_verified(self):        
    #     for prod in self:
    #         state_move = self.env['stock.move'].browse(prod.move_prod_id.id).state
    #         if state_move != 'contre_mesure':
    #             raise exceptions.UserError("Le mouvement lié à cet ordre fabrication n'est pas encore dans l'état contre-mesure")
    #         if prod.hauteur == 0.0 or prod.largeur == 0.0:
    #             raise exceptions.UserError('Les contre-mesures ne doivent pas être vides. Merci de faire remplir par le responsable dans le bon de livraison lié')
    #     self.state = 'verified'






    # Implementation of workflow modified
    @api.multi
    def sheet_verified(self):
        self.state = 'verified'

    @api.multi
    def cancel_validation(self):
        self.state = 'verified'    

    @api.multi
    def button_validate(self):
        self.state = 'validated'


    # Function for checking availlability
    @api.multi
    def action_assign(self):
        super(MrpProduction, self).action_assign()

        if self.availability == 'partially_available':
            self.state = 'confirmed'
        else:
            self.state = 'ready'

    
    # Function for produce
    @api.multi
    def open_produce_product(self):
        self.state = 'progress'
        return super(MrpProduction, self).open_produce_product()

    # Function for set a draft
    @api.multi
    def set_draft(self):
        self.state = 'draft'

        
    