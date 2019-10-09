# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from openerp import tools

class mim_wizard(osv.osv_memory):
    def _get_order_id(self, cr, uid, context=None):
        if context is None: context = {}
        return context.get('order_id', False)
    
    _inherit = 'mim.wizard'
    _columns = {
            'order_id': fields.integer('Order Lines'),
            }
    _defaults = {
              'order_id':_get_order_id,
              }
    
    def order_line_create(self, cr, uid, ids, context=None):
        sale_order_line_obj = self.pool.get('sale.order.line')
        select_type = self.browse(cr, uid, ids, context=context)[0].select_type
        type_fix = self.browse(cr, uid, ids, context=context)[0].type_fixe
        inegalite = self.browse(cr, uid, ids, context=context)[0].inegalite
        vitrage = self.browse(cr, uid, ids, context=context)[0].vitre
        type_vitre = self.browse(cr, uid, ids, context=context)[0].type_vitre
        decoratif = self.browse(cr, uid, ids, context=context)[0].decoratif
        serr = self.browse(cr, uid, ids, context=context)[0].serr
        poigne = self.browse(cr, uid, ids, context=context)[0].poigne
        nb_poigne = self.browse(cr, uid, ids, context=context)[0].nb_poigne
        nb_serr = self.browse(cr, uid, ids, context=context)[0].nb_serr
        oscillo_battant = self.browse(cr, uid, ids, context=context)[0].oscillo_battant
        va_et_vient = self.browse(cr, uid, ids, context=context)[0].va_et_vient
        butoir = self.browse(cr, uid, ids, context=context)[0].butoir
        remplissage_vitre = self.browse(cr, uid, ids, context=context)[0].remplissage_vitre
        cintre = self.browse(cr, uid, ids, context=context)[0].cintre
        triangle = self.browse(cr, uid, ids, context=context)[0].triangle
        division = self.browse(cr, uid, ids, context=context)[0].division
        nb_division = self.browse(cr, uid, ids, context=context)[0].nb_division
        laque = self.browse(cr, uid, ids, context=context)[0].laque
        moustiquaire = self.browse(cr, uid, ids, context=context)[0].moustiquaire
        type_moustiquaire = self.browse(cr, uid, ids, context=context)[0].type_moustiquaire
        tms = self.browse(cr, uid, ids, context=context)[0].tms
        rec_largeur = self.browse(cr, uid, ids, context=context)[0].largeur
        rec_hauteur = self.browse(cr, uid, ids, context=context)[0].hauteur
        intermediaire = self.browse(cr, uid, ids, context=context)[0].intermediaire
        rec_dimension = self.browse(cr, uid, ids, context=context)[0].dimension
        rec_pu_ttc = self.browse(cr, uid, ids, context=context)[0].pu_ttc
        
        rec_qty = self.browse(cr, uid, ids, context=context)[0].quantity
        image = self.browse(cr, uid, ids, context=context)[0].image
        total = self.calcul(cr, uid, ids, rec_largeur, rec_hauteur,rec_dimension, rec_pu_ttc, rec_qty, select_type.id , vitrage.id,
			    type_vitre, decoratif.id,  poigne.id, serr.id,nb_poigne,nb_serr,oscillo_battant,
			    va_et_vient, butoir,remplissage_vitre, cintre, triangle,division,nb_division, laque,
			    moustiquaire, type_moustiquaire, tms, intermediaire, context)
        order_id = self.browse(cr, uid, ids, context=context)[0].order_id
            
        select_type0 = select_type.id
        type_fix0 = type_fix
        inegalite0 = inegalite
        vitrage0 = vitrage.id
        type_vitre0 = type_vitre
        decoratif0 = decoratif.id
        serr0 = serr.id
        poigne0 = poigne.id
        nb_poigne0 = nb_poigne
        nb_serr0 = nb_serr
        oscillo_battant0 = oscillo_battant
        va_et_vient0 = va_et_vient
        butoir0 = butoir
        remplissage_vitre0 = remplissage_vitre
        cintre0 = cintre
        triangle0 = triangle
        division0 = division
        nb_division0 = nb_division
        laque0 = laque
        moustiquaire0 = moustiquaire
        type_moustiquaire0 = type_moustiquaire
        tms0 = tms
        rec_largeur0 = rec_largeur
        rec_hauteur0 = rec_hauteur
        if not intermediaire:
            intermediaire = 'sans'
        intermediaire0 = intermediaire
        rec_dimension0 = rec_dimension
        rec_qty0 = rec_qty
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
        intermdr = ''
        inegalit = ''
        
        if type_vitre:
            if type_vitre=='double':
                simple_double=' double,'
        dec=decoratif.name
        if ((decoratif.name is not None) and(decoratif.name!=False)):
            if dec==u'Compliqué':
                deco=u' compliqué,'
        if intermediaire == 'avec':
            intermdr = u'avec intermédiaire, '
        else : 
            intermdr = u'sans intermédiaire, '
        if inegalite:
            if inegalite == 'egaux':
                inegalit = ''
            if inegalite == u'inegaux':
                inegalit = u'inégaux,'
                
        if ((vitrage.name==False)or(vitrage.name is None)):
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
            if serr.name:
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
            if serr.name:
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
            if serr.name:
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
            if serr.name:
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
            types = u" Porte ouvrante 2VTX  "+"\n - Accessoires :"+" ".join((inegalit+" "+tmss+" "+intermdr+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+" \n"
        
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
        
        types_tmp = types
        #if types == 'Poteau rectangle' or 'Poteau d\'angle' or 'Tendeur':
        if types in ('Poteau rectangle','Poteau d\'angle','Tendeur','Bardage PVC','Projetant'):
            if types == 'Poteau rectangle':
                types = "Poteau rectangle"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+"\n"
            if types == 'Poteau d\'angle':
                types = "Poteau d'angle"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+"\n"
            if types == "Tendeur":
                types = "Tendeur"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+"\n"
            if types == 'Bardage PVC':
                types = "Bardage PVC"+"\n - Accessoires :"+" ".join((tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+"\n"
            if types == 'Projetant':
                poigne_valeur = ''
                nb_poigne_valeur = ''
                if poigne.name:
                    poigne_valeur = poigne.name
                    nb_poigne_valeur = str(nb_poigne)
                    
                serr_valeur = ''
                nb_serr_valeur = ''
                if serr.name:
                    serr_valeur = serr.name
                    nb_serr_valeur = str(nb_serr)
                types = "Projetant"+"\n - Accessoires :"+" ".join((nb_poigne_valeur +" "+poigne_valeur+", "+ nb_serr_valeur +" "+ serr_valeur +" "+tmss+" "+dvs+" "+btr+" "+oscillo+" "+v_et_v+" "+ctr+" "+lq+" "+trgl+" ").split())+vitre+" ".join((simple_double+deco+" "+rempli+" "+mstqr).split())+"\n"
        
        lxh = types
        
        if types_tmp == 'Poteau rectangle':
            if (rec_dimension and rec_pu_ttc):
                lxh=lxh+" \n\t - Dimension : %d x %d \n"%(rec_dimension,rec_pu_ttc,)
        else:
            if(rec_largeur and rec_hauteur):
                lxh=lxh+"- Dimension : %d x %d HT \n"%(rec_largeur,rec_hauteur,)
        
        #description
        name = lxh
        
        res_image = tools.image_resize_image(image, (64, 64), 'base64', 'PNG', False)
        sale_order_line_obj.create(cr, uid, {'product_id':select_type.id,'name': name,'order_id':order_id,
        'product_uom_qty': rec_qty, 'price_subtotal' : total['totalcacher'], 'price_unit': total['totalcacher']/rec_qty,'image':res_image,
        'select_type':select_type0,'largeur':rec_largeur0,'hauteur':rec_hauteur0,'dimension':rec_dimension0,
        'vitre':vitrage0,'type_vitre':type_vitre0,'decoratif' :decoratif0,'poigne' :poigne0,'nb_poigne':nb_poigne0,'serr' :serr0,
        'nb_serr':nb_serr0,'oscillo_battant':oscillo_battant0,'va_et_vient':va_et_vient0,'butoir':butoir0,'remplissage_vitre':remplissage_vitre0,
        'type_fixe':type_fix0,'inegalite':inegalite0,'cintre':cintre0,'triangle':triangle0,'division':division0,'nb_division':nb_division0,
        'laque':laque0,'moustiquaire':moustiquaire0,'tms':tms0,'type_moustiquaire':type_moustiquaire0,'intermediaire':intermediaire0
         })
        
        return True

mim_wizard()

class sale_order(osv.osv):
    ####override de la classe sale_order du module sale pour l'hÃ©ritage####
    _inherit = "sale.order"
    
    ####cette fonction permet de rÃ©cupÃ©rer la rÃ©fÃ©rence du devis en cours de modification par ex SO003####
    def action_mim_wizard(self, cr, uid, ids, context=None):
      
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ctx = dict()
        sujet = self.browse(cr, uid, ids, context=context)[0].name
        #ando
        order_id = self.browse(cr, uid, ids, context=context)[0].id
        #####
        order_ref = sujet[2:]
        ctx.update({
            'default_sujet': 'Devis '+sujet,
            'default_order_ref':order_ref,
            #ando
            'default_order_id' : order_id,
            #####
            
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
sale_order()
#heritage de la classe sale.order.line pour y ajouter les nouvelles colonnes necessaire à la nomenclature 
class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    _columns = {
        
        #'image' : fields.binary('Image'),
        #'select_type': fields.many2one('product.product', string='Type'),
        'largeur':fields.float('Largeur'),
        'hauteur':fields.float('Hauteur'),
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
    }
sale_order_line()
    
