# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import openerp
from openerp import tools
class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _columns = {
                'image': fields.binary('Image'),
                }
class sale_order(osv.osv):
    _inherit = "sale.order"
    _columns = {
                'note': fields.text('Terms and conditions'),
                }
    _defaults = {
                'note':u'''Délais de fabrications : ... semaines après date de confirmation de commande, sous réserve de disponibilité en stock.
Garantie : Tous les accessoires sont garantis UN an.
Mode de paiement :
-    50% à la commande
-    50% avant livraison
Service : Livraison et pose gratuites pour Antananarivo et banlieue proche. A défaut d'électricité, le carburant du groupe électrogène fourni par MIM sera à la charge du client.
Toute modification ultérieure fera l'objet d'une réactualisation de notre offre.
Si cette offre vous convient, merci de nous la renvoyer signée avec la mention "Bon pour accord"'''
                }
sale_order_line()

class mim_wizard(osv.osv_memory):
    _inherit = 'mim.wizard'
    _columns = {
                'image' : fields.binary('Image'),
                }
    
    def onchange_fields(self, cr, uid, ids, largeur, hauteur, dimension, pu_ttc, quantity, select_type, vitre,
            type_vitre,decoratif, poigne, serr,nb_poigne,nb_serr,oscillo_battant,
            va_et_vient, butoir,remplissage_vitre, cintre, triangle,division,nb_division, laque,
            moustiquaire, type_moustiquaire, tms, context=None):
        
        return {'value': self.calcul(cr, uid, ids, largeur, hauteur, dimension, pu_ttc, quantity, select_type, vitre,
            type_vitre,decoratif, poigne, serr,nb_poigne,nb_serr,oscillo_battant,
            va_et_vient, butoir,remplissage_vitre, cintre, triangle,division,nb_division, laque,
            moustiquaire, type_moustiquaire, tms, context)}
        
    def calcul(self, cr, uid, ids, largeur, hauteur, dimension, pu_ttc, quantity, select_type, vitre,
            type_vitre,decoratif, poigne, serr,nb_poigne,nb_serr,oscillo_battant,
            va_et_vient, butoir,remplissage_vitre, cintre, triangle,division,nb_division, laque,
            moustiquaire, type_moustiquaire, tms, context=None):
        
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
        image_name = 'image0.png'
            #si le champ vitre n'es pas vide c'est Ã  dire contient une valeur . Et comme cette valeur est reliÃ©e Ã  l'objet mim.article donc 
        #on doit recupÃ©rer l'objet puis le parcourir pour obtenir l'attribut category_ids : self.pool.get('mim.article').browse(cr, uid, vitre, context=context) . Il suffit en suite de rÃ©cupÃ©rer le prix si id est vrai. Idem pour decoratif, poigne et serrure
        if vitre:
            #raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (vitre))
                categ = self.pool.get('mim.article').browse(cr, uid, vitre, context=context)
                val_vitre = categ.price

        if type_vitre == 'double':
            if vitre:
                val_type_vitre = 2
        else:
            val_vitre = 55000

        if decoratif:
                categ = self.pool.get('mim.article').browse(cr, uid, decoratif, context=context)
                if categ.category_ids.id:
                    val_decoratif = categ.price
    
        if poigne:
                categ = self.pool.get('mim.article').browse(cr, uid, poigne, context=context)
                if categ.category_ids.id:
                    val_poigne = categ.price * nb_poigne
    
        if serr:
                categ = self.pool.get('mim.article').browse(cr, uid, serr, context=context)
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
                prod = self.pool.get('product.product').browse(cr, uid, select_type, context=context)
        
                types = prod.name
                

        if types == 'Coulissante 2VTX':
            image_name='image1.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = (((((largeur*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre*val_triangle)+val_moustiquaire)*val_laque
        #raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (types))
            

        if types == 'Coulissante 1VTL':
            image_name='image2.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((((((largeur*2)*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre/2)*val_laque)+val_moustiquaire

        if types == 'Coulissante 3VTX':
            image_name='image3.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/3*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((((largeur*hauteur)/1000000*(180000*(1+(tms / 100))+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)+val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.025*1.08*val_cintre+val_moustiquaire)*val_laque

        if types == 'Coulissante 4VTX':
            image_name='image4.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = (((largeur*hauteur)/1000000*(180000/2*(1+(tms / 100))*val_remplissage_vitre+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*2+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.05*1.025*1.08*val_cintre*val_laque)+val_moustiquaire
            
    
        if types == 'Porte ouvrante 2VTX':
            image_name='image5.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = (((largeur*hauteur)/1000000*((210222+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+92884+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre*val_laque)+val_moustiquaire

        if types == 'Porte ouvrante 1VTL':
            image_name='image6.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((((largeur*hauteur)/1000000*(210000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+58652+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre+val_moustiquaire)*val_laque
        if types == u'Fenêtre ouvrante 1VTL':
            image_name='image7.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((((largeur*hauteur)/1000000*(210000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+58652+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.15*1.08*val_cintre+val_moustiquaire)*val_laque

        if types == u'Fenêtre ouvrante 2VTX':
            image_name='image8.png'    
            if moustiquaire:
                val_moustiquaire = (((largeur/hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((((largeur*hauteur)/1000000*(210222+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+92884+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir+40000)*1.15*1.08*val_cintre*val_laque)+val_moustiquaire
    
        if types == 'A soufflet':
            image_name='image9.png'
            if division:
                val_total = (((((largeur/nb_division)*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*nb_division
            else:
                if moustiquaire:
                    val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
                val_total = ((((largeur*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms/100))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*val_laque)+val_moustiquaire
        if types == 'Projetant':
            image_name='image10.png'
            if division:
                val_total = (((((largeur/nb_division)*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100)))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*nb_division
            else:
                if moustiquaire:
                    val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
                val_total = ((((largeur*hauteur)/1000000*(163000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms/100))*val_remplissage_vitre+58500+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.1*1.05*1.25*1.08*val_cintre)*val_laque)+val_moustiquaire
            
        if types == 'Fixe':
            image_name='image11.png'    
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((largeur*hauteur)/1000000*(150000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*val_remplissage_vitre*1.15*1.08*val_cintre*val_triangle*val_laque)+val_moustiquaire

        if types == 'Moustiquaire':
            image_name='image12.png'
            cacher = True
            if type_moustiquaire == 'fixe':
                val_total = ((((largeur/nb_division)*hauteur)/1000000*13500)*1.2*1.08*1.4)*nb_division
            if type_moustiquaire == 'coulissante':
                val_total = ((((largeur/nb_division)*hauteur)/1000000*81000)*1.2*1.08)*nb_division

        if types == 'Naco':
            image_name='image13.png'    
            if moustiquaire:
                val_moustiquaire = ((((largeur*hauteur)/1000000*13500)*1.2*1.08*1.4))
            if division:
                val_total =(((largeur/nb_division)*hauteur)/1000000*(150000+val_decoratif+val_autre_vitrage+(3000*(hauteur/100))))*1.15*1.08*val_cintre*val_laque*nb_division
            else:
                val_total =((((largeur*hauteur)/1000000*(150000+val_vitre*val_type_vitre+val_autre_vitrage+(3000*(hauteur/100))))*1.15*1.08*val_cintre*val_laque))+val_moustiquaire


        if types == 'Poteau rectangle':
            image_name='image14.png'
            cacher = True
            if laque == True:
                val_total = ((dimension/1000)*pu_ttc)*val_laque
            if laque == False:
                val_total = ((dimension/1000)*pu_ttc)*1

        if types == 'Poteau d\'angle':
            image_name='image15.png'
            cacher = True
            if laque == True:
                val_total = ((dimension/1000)*pu_ttc)*val_laque
            if laque == False:
                val_total = ((dimension/1000)*pu_ttc)*1

        if types == 'Tendeur':
            image_name='image16.png'
            cacher = True
            if laque == True:
                val_total = ((dimension/1000)*pu_ttc)*val_laque
            if laque == False:
                val_total = ((dimension/1000)*pu_ttc)*1
            
        if types == 'Bardage PVC':
            image_name='image17.png'
            cacher = True
            hidder_autre_option = True 
            val_total = ((largeur*hauteur)/1000000)*45000/1.2
    
        img_path = openerp.modules.get_module_resource('mim_module_add_image', 'static/src/img', (image_name))
        with open(img_path, 'rb') as f:
            image = f.read()
        #res_image = tools.image_resize_image_big(image.encode('base64'))
        res_image = image.encode('base64')
        return {'total' : val_total* quantity ,'totalcacher' : val_total* quantity, 'cacher' : cacher, 'hidder_autre_option': hidder_autre_option,'image': res_image}
    
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
        rec_ref = self.browse(cr, uid, ids, context=context)[0].order_ref
        rec_qty = self.browse(cr, uid, ids, context=context)[0].quantity
        #rec_total = self.browse(cr, uid, ids, context=context)[0].totalcacher
        total = self.calcul(cr, uid, ids, rec_largeur, rec_hauteur,rec_dimension, rec_pu_ttc, rec_qty, select_type.id , vitrage.id,
                type_vitre, decoratif.id,  poigne.id, serr.id,nb_poigne,nb_serr,oscillo_battant,
                va_et_vient, butoir,remplissage_vitre, cintre, triangle,division,nb_division, laque,
                moustiquaire, type_moustiquaire, tms, context)
        image = self.browse(cr, uid, ids, context=context)[0].image
        
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
                
        dec = decoratif.name
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
        
        name = lxh
        res_image = tools.image_resize_image(image, (64, 64), 'base64', 'PNG', False)
        sale_order_line_obj.create(cr, uid, {'product_id':select_type.id,'name': name,'order_id':rec_ref+1, 'product_uom_qty': rec_qty, 'price_subtotal' : total['totalcacher'], 'price_unit': total['totalcacher']/rec_qty,'image':res_image})
        return True
    
mim_wizard()