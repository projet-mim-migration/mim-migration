# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo import tools

class MimWizard(models.TransientModel):
    _inherit = 'mim.wizard'

    def _get_order_id(self):
        context = dict(self._context or {})
        return context.get('order_id', False)
    
    
    order_id = fields.Integer(
        string='Order Lines',
        default=_get_order_id,
    )
    
    
    @api.multi
    def order_line_create(self):
        print('######################################################################')
        print('######################################################################')
        print('##MRP FICHE DE DEBIT##')
        print('######################################################################')
        print('######################################################################')
        
        self.ensure_one()

        sale_order_line_obj = self.env['sale.order.line']
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
        
        rec_qty = self.quantity
        image = self.image
        total = self.calcul()
        order_id = self.order_id
            
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

        sale_order_line_obj.create({
            'product_id' : select_type.id,
            'name' : name,
            'order_id' : order_id,
            'product_uom_qty' : rec_qty, 
            'price_subtotal' : total['totalcacher'], 
            'price_unit' : total['totalcacher']/rec_qty,
            'image' : res_image,
            'select_type' : select_type0,
            'largeur' : rec_largeur0,
            'hauteur' : rec_hauteur0,
            'dimension' : rec_dimension0,
            'vitre' : vitrage0,
            'type_vitre' : type_vitre0,
            'decoratif' : decoratif0,
            'poigne' : poigne0,
            'nb_poigne' : nb_poigne0,
            'serr' : serr0,
            'nb_serr' : nb_serr0,
            'oscillo_battant' : oscillo_battant0,
            'va_et_vient' : va_et_vient0,
            'butoir' : butoir0,
            'remplissage_vitre' : remplissage_vitre0,
            'type_fixe' : type_fix0,
            'inegalite' : inegalite0,
            'cintre' : cintre0,
            'triangle' : triangle0,
            'division' : division0,
            'nb_division' : nb_division0,
            'laque' : laque0,
            'moustiquaire' : moustiquaire0,
            'tms' : tms0,
            'type_moustiquaire' : type_moustiquaire0,
            'intermediaire' : intermediaire0
         })
        
        return True
