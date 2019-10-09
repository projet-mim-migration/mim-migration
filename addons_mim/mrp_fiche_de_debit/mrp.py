# -*- coding: utf-8 -*-
import time

from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp.addons.product import _common
from openerp import tools
#from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.safe_eval import safe_eval
from openerp import netsvc

class mrp_bom_line(osv.osv):
    
    _inherit = 'mrp.bom.line'
    _columns = {
                #'product_qty2': fields.float(u'Quantité d\'article en unité'),
                'ref': fields.char(u'Référence'),
                #'sequence':fields.integer(u'Sequence'),
                'is_accessory': fields.boolean('Est un accesoire'),
                'component_exist':fields.boolean('Composant existe'),
                'component_id':fields.integer(u'Composant'),
                }
    _sql_constraints = [('reference_unique', 'unique(ref)', u'Il y a des doublons dans la colonne référence!')]
    _defaults = {
                 'component_exist':False,
                 'is_accessory':False
                 }
    
    def open_view_component(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        #component_obj = self.pool.get('mrp.component')
        product_id = self.browse(cr, uid, ids, context=context)[0].product_id
        id = self.browse(cr, uid, ids, context=context)[0].id
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'mrp_fiche_de_debit', 'mrp_configuration_component_form_view2')
        view_id = view_ref and view_ref[1] or False,
        component_exist = self.browse(cr, uid, ids, context=context)[0].component_exist
        if not component_exist:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Ajouter les sous-composants',
                'res_model': 'mrp.component',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'new',
                'nodestroy': True,
                'context':{
                           'default_product_parent_id': product_id.id,
                           'default_line_id':id, 
                           'default_component_exist': component_exist,          
                           },
            }
        else:
            component_id = self.browse(cr, uid, ids, context=context)[0].component_id
            return {
                'type': 'ir.actions.act_window',
                'name': 'Modifier les sous-composants',
                'res_model': 'mrp.component',
                'res_id':component_id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'new',
                'nodestroy': True,
            }

mrp_bom_line()
    
class mrp_bom(osv.osv):
    
    _inherit = 'mrp.bom'
    
    def _bom_explode(self, cr, uid, bom, product, factor, properties=None, level=0, routing_id=False, previous_products=None, master_bom=None, context=None):
        """ Finds Products and Work Centers for related BoM for manufacturing order.
        @param bom: BoM of particular product template.
        @param product: Select a particular variant of the BoM. If False use BoM without variants.
        @param factor: Factor represents the quantity, but in UoM of the BoM, taking into account the numbers produced by the BoM
        @param properties: A List of properties Ids.
        @param level: Depth level to find BoM lines starts from 10.
        @param previous_products: List of product previously use by bom explore to avoid recursion
        @param master_bom: When recursion, used to display the name of the master bom
        @return: result: List of dictionaries containing product details.
                 result2: List of dictionaries containing Work Center details.
        """
        uom_obj = self.pool.get("product.uom")
        routing_obj = self.pool.get('mrp.routing')
        master_bom = master_bom or bom


        def _factor(factor, product_efficiency, product_rounding):
            factor = factor / (product_efficiency or 1.0)
            factor = _common.ceiling(factor, product_rounding)
            if factor < product_rounding:
                factor = product_rounding
            return factor

        factor = _factor(factor, bom.product_efficiency, bom.product_rounding)

        result = []
        result2 = []

        routing = (routing_id and routing_obj.browse(cr, uid, routing_id)) or bom.routing_id or False
        if routing:
            for wc_use in routing.workcenter_lines:
                wc = wc_use.workcenter_id
                d, m = divmod(factor, wc_use.workcenter_id.capacity_per_cycle)
                mult = (d + (m and 1.0 or 0.0))
                cycle = mult * wc_use.cycle_nbr
                result2.append({
                    'name': tools.ustr(wc_use.name) + ' - ' + tools.ustr(bom.product_tmpl_id.name_get()[0][1]),
                    'workcenter_id': wc.id,
                    'sequence': level + (wc_use.sequence or 0),
                    'cycle': cycle,
                    'hour': float(wc_use.hour_nbr * mult + ((wc.time_start or 0.0) + (wc.time_stop or 0.0) + cycle * (wc.time_cycle or 0.0)) * (wc.time_efficiency or 1.0)),
                })

        for bom_line_id in bom.bom_line_ids:
            if self._skip_bom_line(cr, uid, bom_line_id, product, context=context):
                continue
            if set(map(int, bom_line_id.property_ids or [])) - set(properties or []):
                continue

            if previous_products and bom_line_id.product_id.product_tmpl_id.id in previous_products:
                raise osv.except_osv(_('Invalid Action!'), _('BoM "%s" contains a BoM line with a product recursion: "%s".') % (master_bom.name,bom_line_id.product_id.name_get()[0][1]))

            quantity = _factor(bom_line_id.product_qty * factor, bom_line_id.product_efficiency, bom_line_id.product_rounding)
            bom_id = self._bom_find(cr, uid, product_id=bom_line_id.product_id.id, properties=properties, context=context)

            #If BoM should not behave like PhantoM, just add the product, otherwise explode further
            if bom_line_id.type != "phantom" and (not bom_id or self.browse(cr, uid, bom_id, context=context).type != "phantom"):
                result.append({
                    'name': bom_line_id.product_id.name,
                    'product_id': bom_line_id.product_id.id,
                    'product_qty': quantity,
                    'product_uom': bom_line_id.product_uom.id,
                    'product_uos_qty': bom_line_id.product_uos and _factor(bom_line_id.product_uos_qty * factor, bom_line_id.product_efficiency, bom_line_id.product_rounding) or False,
                    'product_uos': bom_line_id.product_uos and bom_line_id.product_uos.id or False,
                    
                    #Ajout des nouveaux paramètres
                    'ref':bom_line_id.ref,
                    'sequence':bom_line_id.sequence,
                    'is_accessory':bom_line_id.is_accessory,
                    'line_id':bom_line_id.id
                    #
                })
            elif bom_id:
                all_prod = [bom.product_tmpl_id.id] + (previous_products or [])
                bom2 = self.browse(cr, uid, bom_id, context=context)
                # We need to convert to units/UoM of chosen BoM
                factor2 = uom_obj._compute_qty(cr, uid, bom_line_id.product_uom.id, quantity, bom2.product_uom.id)
                quantity2 = factor2 / bom2.product_qty
                res = self._bom_explode(cr, uid, bom2, bom_line_id.product_id, quantity2,
                    properties=properties, level=level + 10, previous_products=all_prod, master_bom=master_bom, context=context)
                result = result + res[0]
                result2 = result2 + res[1]
            else:
                raise osv.except_osv(_('Invalid Action!'), _('BoM "%s" contains a phantom BoM line but the product "%s" does not have any BoM defined.') % (master_bom.name,bom_line_id.product_id.name_get()[0][1]))

        return result, result2
mrp_bom()

class mrp_production(osv.osv):
    def _get_default_batis(self, cr, uid, ids):
        batis_ids = self.pool.get('mim.article').search(cr, uid, [('name','=','T 60 K B')])
        if not batis_ids:
            raise osv.except_osv('Erreur!', u"Le bâtis T 60 K B par défaut n\'est pas défini dans mim.article!")
        return batis_ids[0]
    
    def test_if_product(self, cr, uid, ids):
        """
        @return: True or False
        """
        res = True
        if self.browse(cr, uid, ids)[0].is_printable:
            for production in self.browse(cr, uid, ids):
                boms = self._prepare_lines(cr, uid, production)[0]
                res = False
                for bom in boms:
                    product = self.pool.get('product.product').browse(cr, uid, bom['product_id'])
                    if product.type in ('product', 'consu'):
                        res = True
        return res
    
    def _get_partner_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for production in self.browse(cr, uid, ids, context=context):
            res[production.id] = production.partner_id.name
        return res
    
    _inherit = 'mrp.production'
    _columns = {
                'largeur': fields.float('Largeur'),
                'hauteur': fields.float('Hauteur'),
                'nbr_barre': fields.float('Nombre total de barres'),
                'product_lines1': fields.one2many('mrp.production.product.component.line', 'production_id', 'Articles'),
                'product_lines2': fields.one2many('mrp.production.product.accessory.line', 'production_id', 'Accessoires'),
                'is_printable':fields.boolean('Fiche de débit standard'),
                
                'dimension':fields.float('Dimension'),
                'vitre': fields.many2one('mim.article', string='Vitre'),
                'type_vitre':fields.selection([('simple','Simple'),('double','Double')], string=""),
                'decoratif' : fields.many2one('mim.article', string=u'Décoratif'),
                'poigne' : fields.many2one('mim.article', string=u'Poignée'),
                'nb_poigne':fields.integer('Nombre'),
                'serr' : fields.many2one('mim.article', string='Serrure'),
                'nb_serr':fields.integer('Nombre'),
                'oscillo_battant':fields.boolean('Oscillo-battant'),
                'va_et_vient':fields.boolean('Va et vient'),
                'butoir':fields.boolean('Butoir'),
                'remplissage_vitre':fields.selection([('standard','Standard'),('pleine_2_3','2/3 pleine'),('pleine_1_2','1/2 pleine'),('pleine_1_3','1/3 pleine'),('pleine_bardage','Pleine/bardage')], string="Remplissage vitre"),
                'type_fixe':fields.selection([('imposte','Imposte'),('soubassement','Soubassement'),('lateral',u'Latéral')], string="Type Fixe"),
                'inegalite':fields.selection([('egaux','Egaux'),('inegaux',u'Inégaux')], string=u"Inégalité"),
                #'type_poteau':fields.selection([('poteau_rect','Poteau rectangle'),('poteau_angle','Poteau d\'angle'),('tendeur','Tendeur'),], string="Poteau Rect / Angle / Tendeur"),
                'cintre':fields.boolean(u'Cintré'),
                'triangle':fields.boolean('Triangle'),
                'division':fields.boolean('Division'),
                'nb_division':fields.integer('Nombre division'),
                'laque':fields.boolean(u'Laqué'),
                'moustiquaire':fields.boolean('Moustiquaire'),
                'tms':fields.float('TMS'),
                'type_moustiquaire':fields.selection([('fixe','Fixe'),('coulissante','Coulissante')], string="Type de moustiquaire"),
                'intermediaire': fields.selection([('sans',u'Sans intermédiaire'),('avec',u'Avec intermédiaire')], string=u"Intermédiaire"),
                'type_intermediaire': fields.selection([('vert','Vertical'),('horiz','Horizontal')], string=u"Type intermédiaire"),
                
                'is_calculated':fields.boolean('Fiche de débit calculée'),
                'longueur_barre': fields.float('Longueur barre / unité ',required=True),
                'description':fields.char('Description'),
                'partner_id': fields.many2one('res.partner', 'Client'),
                
                'style':fields.selection([('fr',u'A la française'),('en','A l\'anglaise')], string="Style"),
                'batis_id': fields.many2one('mim.article', string=u'Bâtis', domain=[('category_ids', '=', u'Bâtis')]),
                
                'state': fields.selection(
                [('draft', 'New'), ('verified', u'Fiche vérifiée'),('validated', u'Fiche de débit validée'), ('cancel', 'Cancelled'), ('picking_except', 'Picking Exception'), ('confirmed', 'Awaiting Raw Materials'),
                ('ready', 'Ready to Produce'), ('in_production', 'Production Started'), ('done', 'Done')],
                string='Status', readonly=True,
                track_visibility='onchange',
                help="When the production order is created the status is set to 'Draft'.\n\
                    If the order is confirmed the status is set to 'Waiting Goods'.\n\
                    If any exceptions are there, the status is set to 'Picking Exception'.\n\
                    If the stock is available then the status is set to 'Ready to Produce'.\n\
                    When the production gets started then the status is set to 'In Production'.\n\
                    When the production is over, the status is set to 'Done'."),
                #date plannifie modifiable dans tous les etats sauf dans Termine
                'date_planned': fields.datetime('Scheduled Date', required=True, select=1, readonly=False, states={'done':[('readonly',True)]}),    
                #permettre dediter les lignes des articles prevus
                'product_lines': fields.one2many('mrp.production.product.line', 'production_id', 'Scheduled goods',
                 readonly=True, states={'draft':[('readonly',False)]}),
                
                #champ permettant de prendre le nom du client
                'partner_name': fields.function(_get_partner_name, type='char',string='Nom du client'),
                }
    _defaults = {
                 'nbr_barre':0.0,
                 'is_printable':False,
                 'is_calculated':False,
                 'longueur_barre':5800.0,
                 'style': 'fr',
                 'nb_division':1.0,
                 #'batis_id':_get_default_batis,
                }
    
    def action_produce(self, cr, uid, production_id, production_qty, production_mode, wiz=False, context=None):
        #Redéfintion de la fonction action_produce() pour mettre stock.move à l'etat disponible
        if production_mode == 'consume_produce':
            self.pool.get('mrp.production').set_move_available(cr, uid, production_id, context=context)
        elif production_mode == 'consume':
            for production in self.browse(cr, uid, [production_id], context=context):
                wf_service = netsvc.LocalService("workflow")
                if production.move_prod_id.id:
                    wf_service.trg_validate(uid, 'stock.move', production.move_prod_id.id, 'flow_sheet', cr)
                else:
                    raise osv.except_osv(('Erreur'), (u'Cet ordre de fabrication n\'est liée à aucun mouvement de stock (stock.move)'))
        return super(mrp_production, self).action_produce(cr, uid, production_id, production_qty, production_mode, wiz=wiz, context=context)
    
    def round_float(self, cr, uid, ids, qty, context=None):
        s = str(qty)
        t = s.split('.')
        dec = 0
        if int(t[1])>0:
            dec = 1
        res = int(t[0]) + dec
        return res
    
    #Fonction permettant de calculer le nombre de barres en fonction de la quatité en mm de barres  
    def get_nbr_barres(self, cr, uid, ids, qty_mm, context=None):
        len_barre = self.browse(cr, uid, ids, context=context)[0].longueur_barre
        #len_barre est la longueur d'une barre en mm par unité
        qty_barres = qty_mm/len_barre
        return self.round_float(cr, uid, ids, qty_barres, context)
    
    def _action_compute_lines(self, cr, uid, ids, properties=None, context=None):
        # Compute product_lines and workcenter_lines from BoM structure
        #@return: product_lines
        

        if properties is None:
            properties = []
        results = []
        prod_line_obj = self.pool.get('mrp.production.product.line')
        workcenter_line_obj = self.pool.get('mrp.production.workcenter.line')
        
        #Modification ando
        prod_line_obj1 = self.pool.get('mrp.production.product.component.line')
        prod_line_obj2 = self.pool.get('mrp.production.product.accessory.line')
        #prod_line_obj3 = self.pool.get('mrp.production.product.all.component.line')
        
        for production in self.browse(cr, uid, ids, context=context):
            #unlink product_lines
            prod_line_obj.unlink(cr, SUPERUSER_ID, [line.id for line in production.product_lines], context=context)
            
            
            #ando unlink product_lines1 components
            prod_line_obj1.unlink(cr, SUPERUSER_ID, [line.id for line in production.product_lines1], context=context)
            
            #unlink product_lines2 accessories
            prod_line_obj2.unlink(cr, SUPERUSER_ID, [line.id for line in production.product_lines2], context=context)
            #########################
            
            
            #unlink workcenter_lines
            workcenter_line_obj.unlink(cr, SUPERUSER_ID, [line.id for line in production.workcenter_lines], context=context)
            
            res = self._prepare_lines(cr, uid, production, properties=properties, context=context)
            results = res[0] # product_lines
            results2 = res[1] # workcenter_lines
            
            #ando Calcul dynamique de la quatité des composants
            product = self.browse(cr, uid, ids, context=context)[0]
            parent_id = product.product_id.id
            qty = product.product_qty
            largeur = product.largeur
            hauteur = product.hauteur
            tms = product.tms
            localdict = {}
            localdict['largeur'] = largeur
            localdict['hauteur'] = hauteur
            localdict['tms'] = tms
            localdict['result'] = None
            localdict['style'] = product.style
            localdict['vitre'] = product.remplissage_vitre
            
            #Mise à jour
            if not product.vitre :
                localdict['type_vitre'] = 0
            else:localdict['type_vitre'] = product.vitre.id
            
            localdict['inter'] = product.intermediaire
            localdict['moust'] = product.moustiquaire
            
            localdict['div'] = product.division
            
            if not product.nb_division :
                localdict['nb_div'] = 1.0
            else:localdict['nb_div'] = product.nb_division
            
            if not product.type_intermediaire or product.type_intermediaire=='vert':
                localdict['type_inter'] = 'vert'
            else:localdict['type_inter'] = 'horiz'
            
            localdict['batis'] = product.batis_id.name
            
            component = self.pool.get('mrp.component')
            #all_component = []
            l = {}
            for line in results:
                line_id = line['line_id']
                list_id = component.search(cr, uid, [('line_id','=',line_id)])
                if list_id:
                    for c in component.browse(cr, uid, list_id, context=context):
                        total1 = 0.0
                        total2 = 0.0
                        
                        len_total0 = 0.0
                        len_unit0 =0.0
                        qty_total0 = 0.0
                        #Insértion de tous les sous-composants pour l'impression
                        for s in c.sub_component_ids:
                            localdict['Q'] = qty
                            
                            safe_eval(s.python_product_qty, localdict, mode='exec', nocopy=True)
                            product_qty = float(localdict['result'])
                            ##################################
                            l['production_id'] = production.id
                            l['product_qty'] = product_qty
                            
                            localdict['QU'] = product_qty
                            
                            product_qty0 = product_qty
                            
                            safe_eval(s.python_product_qty_total, localdict, mode='exec', nocopy=True)
                            product_qty_total = float(localdict['result'])
                            
                            l['product_qty_total'] = product_qty_total
                            #l['product_qty_total'] = qty * l['product_qty']
                            
                            qty_total0 = product_qty_total
                            
                            localdict['QT'] = l['product_qty_total']
                            
                            total2 = total2 + l['product_qty_total']
                            if not line['is_accessory']:
                                l['ref'] = c.product_parent_id.ref
                                l['name'] = s.name
                                safe_eval(s.python_len_unit, localdict, mode='exec', nocopy=True)
                                len_unit = float(localdict['result'])
                                l['len_unit'] = len_unit
                                
                                localdict['LU'] = l['len_unit']
                                
                                #l['len_total'] = l['len_unit'] * l['product_qty_total']
                                
                                safe_eval(s.python_len_total, localdict, mode='exec', nocopy=True)
                                len_total = float(localdict['result'])
                                
                                l['len_total'] = len_total
                                
                                len_total0 = len_total
                                
                                total1 = total1 + l['len_total']
                                
                                LU = l['len_unit']
                                LT = l['len_total']
                                
                                len_unit0 = l['len_unit']
                                
                                if l['len_total']!=0.0:
                                    prod_line_obj1.create(cr, uid, l.copy())
                            else:
                                if l['product_qty_total']!=0.0:
                                    l['ref'] = c.product_parent_id.name
                                    l['name'] = s.name
                                    prod_line_obj2.create(cr, uid, l.copy())
                            l = {}
                            
                        if not line['is_accessory']:
                            uom = c.product_parent_id.uom_id.name
                            ref = c.product_parent_id.ref
                            len_barre = self.browse(cr, uid, ids, context=context)[0].longueur_barre
                            
                            if uom == 'Barre':
                                
                                if ref !='P50-MB':
                                    line['product_qty'] = self.get_nbr_barres(cr, uid, ids, total1, context=context)
                                else:
                                    var = (LU/100.0)*LT*qty_total0/len_barre
                                    line['product_qty'] = self.round_float(cr, uid, ids, var, context)
                            
                            else:
                                line['product_qty'] = (LU * LT * product_qty_total)/10000.0
                            
                        else: line['product_qty'] = total2
                        ##########################################
                        
            #for move_lines in production.move_lines:
            # reset product_lines in production order    
            for line in results:
                if line['product_qty'] !=0.0:
                    line['production_id'] = production.id
                    prod_line_obj.create(cr, uid, line)  
                                
            #reset workcenter_lines in production order
            for line in results2:
                line['production_id'] = production.id
                workcenter_line_obj.create(cr, uid, line)
                
            prod_obj = self.pool.get('mrp.production')
            prod_obj.write(cr, uid, [ids[0]], {'is_calculated':True}, context=context) 
            
        return results
    
    def set_move_available(self, cr, uid, production_id, context=None):
        #Rendre disponible la stock_move lié à l'ordre de fabrication
        production = self.browse(cr, uid, production_id, context=context)
        wf_service = netsvc.LocalService("workflow")
        move_obj = self.pool.get('stock.move')
        if production.move_prod_id.id:
            #===================================================================
            # #creation du mouvement de l'emplacement inventaire vers WH/STOCK, mise à jour inventaire
            # move_obj.modifier_inventaire(cr, uid, [production.move_prod_id.id], context=context)
            #===================================================================
            wf_service.trg_validate(uid, 'stock.move', production.move_prod_id.id, 'force_assign', cr)
        else:
            raise osv.except_osv(('Erreur'), (u'Cette ordre de fabrication n\'est liée à aucun mouvement de stock (stock.move)'))
        return True
    
    def set_draft(self, cr, uid, ids, context=None):
        req = """UPDATE wkf_workitem w 
            SET act_id = (SELECT a.id FROM wkf_activity a WHERE a.wkf_id=(SELECT wkf.id FROM wkf WHERE wkf.name='mrp.production.basic') AND a.name='draft') 
            WHERE w.inst_id = (SELECT i.id FROM wkf_instance i WHERE i.res_id={0} AND i.res_type='mrp.production')""".format(ids[0])
        cr.execute(req)
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
    #Redefintion, ne pas modifier le location_id du mouvement stock.move lié même si il est différent de location_dest_id du MO     
    def action_ready(self, cr, uid, ids, context=None):
        """ Changes the production state to Ready and location id of stock move.
        @return: True
        """
        move_obj = self.pool.get('stock.move')
        self.write(cr, uid, ids, {'state': 'ready'})

        for production in self.browse(cr, uid, ids, context=context):
            if not production.move_created_ids:
                self._make_production_produce_line(cr, uid, production, context=context)

            #if production.move_prod_id and production.move_prod_id.location_id.id != production.location_dest_id.id:
                #move_obj.write(cr, uid, [production.move_prod_id.id],
                        #{'location_id': production.location_dest_id.id})
        return True
    
    def action_verified(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('stock.move')
        for prod in self.browse(cr, uid, ids, context):
            state_move = move_obj.browse(cr, uid, prod.move_prod_id.id, context).state
            if state_move!='contre_mesure':
                raise osv.except_osv(('Erreur'), (u"Le mouvement lié à cet ordre fabrication n'est pas encore dans l'état contre-mesure"))
            if prod.hauteur==0.0 or prod.largeur==0.0:
                raise osv.except_osv(('Erreur'), (u'Les contre-mesures ne doivent pas être vides. Merci de faire remplir par le responsable dans le bon de livraison lié'))
        self.write(cr, uid, ids, {'state': 'verified'})
    
mrp_production()

class mrp_sub_component(osv.osv):
    _name = 'mrp.sub.component'
    _columns = {
                'name': fields.char(u'Désignation'),
                'python_product_qty': fields.text(u'Quantité unitaire(QU)',required=True),
                'python_product_qty_total': fields.text(u'Quantité total (QT)',required=True),
                'python_len_unit': fields.text(u'Longueur unitaire (LU)',required=True),
                'python_len_total': fields.text(u'Longueur total (LT)',required=True),
                'component_id':fields.many2one('mrp.component','Sous-composants', ondelete='cascade'),
                }
    _defaults = {
                 'python_product_qty': 'result=0.0',
                 'python_product_qty_total': 'result=QU*Q',
                 'python_len_unit': 'result=0.0',
                 'python_len_total': 'result=LU*QT',
                 }
mrp_sub_component()

class mrp_component(osv.osv):
    _name = 'mrp.component'
    def _get_product_parent_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('product_parent_id', False)
    def _get_line_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('line_id', False)
    def _get_component_exist(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('component_exist', False)
    _columns = {
                'product_parent_id': fields.many2one('product.product','Article parent', ondelete='cascade'),
                'sub_component_ids':fields.one2many('mrp.sub.component','component_id','Sous-composants'),
                'line_id':fields.many2one('mrp.bom.line','Bom line parent', ondelete='cascade'),
                'component_exist':fields.boolean('Composant existe'),
                'variable': fields.text('Variables utilisables',help=u'Ces variables sont utilisables dans les calculs en code python'),
                }
    _defaults = {
                 'product_parent_id':_get_product_parent_id,
                 'line_id':_get_line_id,
                 'component_exist':_get_component_exist,
                 'variable':u'''Q : Quantité article parent, largeur : 
                 Largeur de l'article, hauteur : Hauteur de l'article, QU : Quantité unitaire, QT : Quantité total, 
                 LU : Longueur unitaire, style : fr ou en, vitre : standard, pleine_bardage, pleine_2_3, pleine_1_2, pleine_1_3 (remplissage vitre)''',
                 }
    
    #Cette fonction permet de sauvegarder pour la première fois le contenu 
    #du sous composant mrp_component après ce sera l fonction write sera utilisée car component_exist est à True
    def save_component(self, cr, uid, ids, context=None):
        comp_obj = self.pool.get('mrp.component')
        bom_line_obj = self.pool.get('mrp.bom.line')
        comp = self.browse(cr, uid, ids, context=context)[0]
        
        vals = {
                'product_parent_id': comp.product_parent_id.id,
                'line_id':comp.line_id.id,
                'component_exist':True,
                }     
        comp_obj.write(cr, uid, [ids[0]], vals, context=context) 
        #component_id est nécéssaire pour réouvrir l'objet mrp_component (res_id) avec la fonction de mrp_bom_line open_view_component()
        #component_exist pour dire que le sous composant a déjà été créé
        val = {'component_exist':True,'component_id':ids[0]}
        bom_line_obj.write(cr, uid, [comp.line_id.id], val, context=context)   
        
        return {'type': 'ir.actions.act_window_close'}    
mrp_component()

class mrp_production_product_line(osv.osv):
    _inherit = 'mrp.production.product.line'
    _columns = {
        'is_accessory': fields.boolean('Est un accesoire'),
        'line_id':fields.many2one('mrp.bom.line','Bom line parent', ondelete='cascade'),
        }
    
    def product_id_change(self, cr, uid, ids, product_id, context=None):
        vals = {}
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            vals = {'product_uom':product.uom_id.id,'name':product.name}
        return {'value':vals}
        
mrp_production_product_line()

#Cette classe servira à stocker les composants de la nomenclature
class mrp_production_product_component_line(osv.osv):
    _name = 'mrp.production.product.component.line'
    #_inherit = 'mrp.production.product.line'
    _description = 'Production component'
    _columns = {
        'ref': fields.char(u'Référence'),       
        'name': fields.char(u'Déscription'),
        'product_qty': fields.float(u'Quantité unitaire'),
        'product_qty_total': fields.float(u'Quantité total'),
        'len_unit': fields.float(u'Longueur unitaire'),
        'len_total': fields.float(u'Longueur total'),
        'production_id': fields.many2one('mrp.production', 'Production Order', select=True, ondelete='cascade'),
        }
mrp_production_product_component_line()

#Cette classe servira à stocker les accessoires de la nomenclature
class mrp_production_product_accessory_line(osv.osv):
    _name = 'mrp.production.product.accessory.line'
    #_inherit = 'mrp.production.product.line'
    _description = 'Production accessory'
    _columns = {
        'ref': fields.char(u'Référence'),       
        'name': fields.char(u'Déscription'),
        'product_qty': fields.float(u'Quantité unitaire'),
        'product_qty_total': fields.float(u'Quantité total'),
        'production_id': fields.many2one('mrp.production', 'Production Order', select=True, ondelete='cascade'),
        }
mrp_production_product_accessory_line()