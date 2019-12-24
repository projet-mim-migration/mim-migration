# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from odoo.tools.safe_eval import safe_eval


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
         ('cancel', 'Cancelled'),
         ('picking_except', 'Picking Exception')], 
        string='State',
        default='draft',
        copy=False,
        track_visibility='onchange'
    )
    product_uom_id = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        oldname='product_uom', readonly=True, required=True,
        states={'draft': [('readonly', False)]}
    )
    # date plannifie modifiable dans tous les etats sauf dans Termine
    date_planned_start = fields.Datetime(
        'Scheduled Date', 
        required=True, 
        select=1, 
        readonly=False, 
        states={'done':[('readonly',True)]}
    )
    # champ permettant de prendre le nom du client
    partner_name = fields.Char(
        string='Nom du client',
        compute=_get_partner_name
    )
    move_prod_id = fields.Many2one(
        'stock.move', 
        'Product Move', 
        readonly=True, 
        copy=False
    )

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

    def _round_float(self, qty):
        s = str(qty)
        t = s.split('.')
        dec = 0
        
        if int(t[1]) > 0:
            dec = 1
        
        res = int(t[0]) + dec
        
        return res
    
    #Fonction permettant de calculer le nombre de barres en fonction de la quatité en mm de barres  
    @api.multi
    def _get_nbr_barres(self, qty_mm):
        self.ensure_one()

        len_barre = self.longueur_barre
        # len_barre est la longueur d'une barre en mm par unité
        qty_barres = qty_mm / len_barre
        return self._round_float(qty_barres)
    

    # Calcul for the raw material of a product
    @api.multi
    def _calcul_raw_material(self):
        self.ensure_one()

        localdict = {
            'Q': self.product_qty,
            'largeur': self.largeur,
            'hauteur': self.hauteur,
            'tms': self.tms,
            'result': None,
            'style': self.style,
            'vitre': self.remplissage_vitre,
            'inter': self.intermediaire,
            'moust': self.moustiquaire,
            'div': self.division,
            'batis': self.batis_id.name,
        }
        # Mise à jour
        if not self.vitre:
            localdict['type_vitre'] = 0
        else:
            localdict['type_vitre'] = self.vitre.id
        
        if not self.nb_division:
            localdict['nb_div'] = 1.0
        else:
            localdict['nb_div'] = self.nb_division
        
        if not self.type_intermediaire or self.type_intermediaire=='vert':
            localdict['type_inter'] = 'vert'
        else:
            localdict['type_inter'] = 'horiz'
                
        l = {}
        # The raw material for the product
        for raw_material in self.bom_id.bom_line_ids:
            for component in self.env['mrp.component'].search([('line_id', '=', raw_material.id)]):
                total1 = 0.0
                total2 = 0.0
                
                len_total0 = 0.0
                len_unit0 =0.0
                qty_total0 = 0.0
                for sub_component in component.sub_component_ids:
                    safe_eval(sub_component.python_product_qty, localdict, mode='exec', nocopy=True)
                    product_qty = float(localdict['result'])

                    l['production_id'] = self.id
                    l['product_qty'] = product_qty
                            
                    localdict['QU'] = product_qty
                            
                    product_qty0 = product_qty

                    safe_eval(sub_component.python_product_qty_total, localdict, mode='exec', nocopy=True)
                    product_qty_total = float(localdict['result'])
                            
                    l['product_qty_total'] = product_qty_total
                            
                    qty_total0 = product_qty_total
                            
                    localdict['QT'] = l['product_qty_total']

                    total2 = total2 + l['product_qty_total']
                    
                    if not raw_material.is_accessory:
                        l['ref'] = component.product_parent_id.ref
                        l['name'] = sub_component.name
                        
                        safe_eval(sub_component.python_len_unit, localdict, mode='exec', nocopy=True)
                        len_unit = float(localdict['result'])
                        
                        l['len_unit'] = len_unit
                        localdict['LU'] = l['len_unit']
                        
                        safe_eval(sub_component.python_len_total, localdict, mode='exec', nocopy=True)
                        len_total = float(localdict['result'])
                        
                        l['len_total'] = len_total
                        len_total0 = len_total
                        
                        total1 = total1 + l['len_total']
                        
                        LU = l['len_unit']
                        LT = l['len_total']
                        
                        len_unit0 = l['len_unit']
                        
                        if l['len_total'] != 0.0:
                            self.env['stock.move.component.line'].create(l.copy())
                    else:
                        if l['product_qty_total'] != 0.0:
                            l['ref'] = component.product_parent_id.name
                            l['name'] = sub_component.name
                            self.env['stock.move.accessory.line'].create(l.copy())
                    
                    l = {}
                  
                if not raw_material.is_accessory:
                    uom = component.product_parent_id.uom_id.name
                    ref = component.product_parent_id.ref
                    len_barre = self.longueur_barre
                    
                    if uom == 'Barre':
                        if ref != 'P50-MB':
                            self.move_raw_ids.filtered(lambda x: x.product_id == raw_material.product_id).product_uom_qty = self._get_nbr_barres(total1)
                        else:
                            var = (LU / 100.0) * LT * qty_total0 / len_barre
                            self.move_raw_ids.filtered(lambda x: x.product_id == raw_material.product_id).product_uom_qty = self._round_float(var)
                            
                    else:
                        self.move_raw_ids.filtered(lambda x: x.product_id == raw_material.product_id).product_uom_qty = (LU * LT * product_qty_total) / 10000.0

                else:
                    self.move_raw_ids.filtered(lambda x: x.product_id == raw_material.product_id).product_uom_qty = total2

        
        self.is_calculated = True

    # Delete the raw material with zero or negative quantity when produce
    @api.multi
    def open_product_produce(self):
        for raw_material in self.move_raw_ids:
            if raw_material.product_qty <= 0:
                raw_material.state = 'draft'
                raw_material.sudo().unlink()
        return super(MrpProduction, self).open_product_produce()

    # Implementation of workflow modified
    @api.multi
    def sheet_verified(self):
        state_move = self.move_prod_id.state
        if state_move != 'contre_mesure':
            raise exceptions.UserError("Le mouvement lié à cet ordre fabrication n'est pas encore dans l'état contre-mesure")
        if self.hauteur == 0.0 or self.largeur == 0.0:
            raise exceptions.UserError('Les contre-mesures ne doivent pas être vides. Merci de faire remplir par le responsable dans le bon de livraison lié')
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


    # Function for set a draft
    @api.multi
    def set_draft(self):
        self.state = 'draft'

        
    @api.model
    def create(self, values):
        production = super(MrpProduction, self).create(values)
        production._calcul_raw_material()
        return production

    # Function for re-calculate the raw material
    @api.multi
    def calculate(self):
        for x in self.env['stock.move.component.line'].search([('production_id', '=', self.id)]):
            x.unlink()
        for x in self.env['stock.move.accessory.line'].search([('production_id', '=', self.id)]):
            x.unlink()
        self._calcul_raw_material()

    # Function to mark the production done
    @api.multi
    def button_mark_done(self):
        self.ensure_one()

        self.move_prod_id.state = 'assigned'

        if all(x.state == 'assigned' for x in self.move_prod_id.picking_id.move_lines):
            for move in self.move_prod_id.picking_id.move_lines:
                move.state = 'confirmed'
                self.move_prod_id.picking_id.action_assign()
        
        super(MrpProduction, self).button_mark_done()
        
        
        
        

        
        



        
