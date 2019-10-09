# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import openerp

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
                'major1': fields.float('Majoration du client'),
                }
    _defaults = {
                 'major1': 0.0,
                 }

class res_users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'
    _columns = {
        'major2': fields.float('Majoration du vendeur'),
    }
    _defaults = {
                 'major2': 0.0,
                 }

class mim_wizard(osv.osv_memory):
   
    _inherit = 'mim.wizard'
    
    def calcul(self, cr, uid, ids, largeur, hauteur, dimension, pu_ttc, quantity, select_type, vitre,
            type_vitre,decoratif, poigne, serr,nb_poigne,nb_serr,oscillo_battant,
            va_et_vient, butoir,remplissage_vitre, cintre, triangle,division,nb_division, laque,
            moustiquaire, type_moustiquaire, tms, intermediaire, context=None):
             
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
                #image_name='image7.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((((((largeur*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre*val_triangle)+val_moustiquaire)*val_laque) * 1.10
            #raise osv.except_osv('Error!','Please define sales journal for this company: "%s" .' % (types))
                
        if types == 'Coulissante 1VTL':
                #image_name='image2.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = (((((((largeur*2)*hauteur)/1000000*(170000+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*(1+(tms / 100))*val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*0.95*1.1*1.08*val_cintre/2)*val_laque)+val_moustiquaire) * 1.10

        if types == 'Coulissante 3VTX':
                #image_name='image3.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/3*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = (((((largeur*hauteur)/1000000*(180000*(1+(tms / 100))+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)+val_remplissage_vitre)+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.025*1.08*val_cintre+val_moustiquaire)*val_laque) * 1.10

        if types == 'Coulissante 4VTX':
                #image_name='image4.png'
            if moustiquaire:
                val_moustiquaire = (((largeur/2*hauteur)/1000000*13500)*1.2*1.08*1.4)
            val_total = ((((largeur*hauteur)/1000000*(180000/2*(1+(tms / 100))*val_remplissage_vitre+val_vitre*val_type_vitre+val_decoratif+val_autre_vitrage)*2+29700+val_poigne+val_serr+val_oscillo_battant+val_va_et_vient+val_butoir)*1.05*1.025*1.08*val_cintre*val_laque)+val_moustiquaire) * 1.10
            
    
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
                 
        img_path = openerp.modules.get_module_resource('mim_module_add_image', 'static/src/img', (image_name))
        with open(img_path, 'rb') as f:
            image = f.read()
        #res_image = tools.image_resize_image_big(image.encode('base64'))
        res_image = image.encode('base64')
    
#         return {'total' : val_total* quantity* 1.10 ,'totalcacher' : val_total* quantity* 1.10, 'cacher' : cacher, 'hidder_autre_option': hidder_autre_option,'image': res_image}
        #majoration du prix par rapport au vendeur et au client
        order_obj = self.pool.get('sale.order').browse(cr, uid, [context.get('active_id',False)])
        maj1 = order_obj.partner_id.major1 / 100
        maj2 = order_obj.user_id.major2 / 100
        maj_globale = 0.0
        if order_obj.company_id:
            maj_globale = order_obj.company_id.maj_globale / 100
        
        return {
                'total' : ((val_total* quantity* 1.10) * (1 + maj1 + maj2)) * (1 + maj_globale),
                'totalcacher' : ((val_total* quantity* 1.10) * (1 + maj1 + maj2)) * (1 + maj_globale), 
                'cacher' : cacher, 
                'hidder_autre_option': hidder_autre_option,
                'image': res_image
                }
mim_wizard()

class sale_order(osv.osv):
    
    _inherit = "sale.order"
    
    _columns = {
                'monnaie_lettre' : fields.char('Total en toute lettre',size =128),
                'maj_globale': fields.float('Majoration globale'),
                'maj_note': fields.text('Note sur la majoration'),
                }
    _defaults = {
                 'maj_globale': 0.0,
             }
    
    #ajout commentaire si la/les majorations existent
    def create(self, cr, uid, vals, context=None):
        #your code
        res_id = super(sale_order, self).create(cr, uid, vals, context=context)
        #your code
        major1 = self.browse(cr, uid, res_id, context=context)[0].partner_id.major1
        major2 = self.browse(cr, uid, res_id, context=context)[0].user_id.major2
        maj_globale = self.browse(cr, uid, res_id, context=context)[0].company_id.maj_globale
        majoration_text = ""
        
#         if(maj_globale != 0.0):
#             majoration_text += "Majoration globale "
#         if(major1 != 0.0):
#             if(majoration_text != ""):
#                 majoration_text += " , Majoration client "
#             else:
#                 majoration_text += "Majoration client "
#         if(major2 != 0.0):
#             if(majoration_text != ""):
#                 majoration_text += " , Majoration vendeur "
#             else:
#                 majoration_text += "Majoration vendeur"
                
        if(major1 != 0.0 or major2 != 0.0):
            majoration_text += "Conforme aux calculs"
            self.message_post(cr, uid, res_id, body = majoration_text, context=context)
        return res_id
    
sale_order()
