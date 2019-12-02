# -*- coding: utf-8 -*-

from odoo import models, fields, api




class stock_picking(models.Model):
    _inherit = "stock.picking"
    
    pose_duree = fields.Float(string='Durée de la pose (jours)', default = 0.0)
    test_groupe = fields.Boolean(string='Est-ce dans le groupe', default = True)
    

    @api.onchange("pose_duree")
    def on_change_fields(self):
        duree_pose = self.pose_duree
        self.env.cr.execute("SELECT res_groups.id FROM res_groups WHERE res_groups.name='Groupe modification date de livraison'")
        res1 = self.env.cr.dictfetchone()
        id_group = res1 ['id']
        self.env.cr.execute("SELECT res_groups_users_rel.uid FROM res_groups_users_rel WHERE res_groups_users_rel.gid={0}".format(id_group))
        res2 = self.env.cr.fetchall()
        list_uid=[]
        value = {}
        for x in range(len(res2)):
            list_uid.append(res2[x][0])
        if self.env.uid in list_uid:
            value['test_groupe'] = True
        else:
            value['test_groupe'] = False
            value['pose_duree'] = duree_pose
        return {'value':value}


#class stock_picking_out(models.Model):
#    _inherit = "stock.picking.out"
#    
#    pose_duree = fields.float(string='Durée de la pose (jours)', default = 0.0)
#    test_groupe = fields.boolean(string='Est-ce dans le groupe', default = True)
#    
#    @api.onchange("pose_duree")
#    def on_change_fields(self):
#        duree_pose = self.pose_duree
#        self.env.cr.execute("SELECT res_groups.id FROM res_groups WHERE res_groups.name='Groupe modification date de livraison'")
#        res1 = self.env.cr.dictfetchone()
#        id_group = res1 ['id']
#        self.env.cr.execute("SELECT res_groups_users_rel.uid FROM res_groups_users_rel WHERE res_groups_users_rel.gid={0}".format(id_group))
#        res2 = self.env.cr.fetchall()
#        list_uid=[]
#        value = {}
#        for x in range(len(res2)):
#            list_uid.append(res2[x][0])
#        if self.uid in list_uid:
#            value['test_groupe'] = True
#        else:
#            value['test_groupe'] = False
#            value['pose_duree'] = duree_pose
#        print("##########################################################################")
#        print (value)
#        print("##########################################################################")
#        
#        return {'value':value}
