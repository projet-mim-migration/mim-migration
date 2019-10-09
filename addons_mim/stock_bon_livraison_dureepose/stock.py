# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
                'pose_duree': fields.float(string='Durée de la pose (jours)'),
                'test_groupe': fields.boolean(string='Est-ce dans le groupe'),
                }
    _defaults = {
                 'pose_duree':0.0,
                 'test_groupe':True,
                }
    def on_change_fields(self, cr, uid, ids, context=None):
        duree_pose = self.browse(cr, uid, ids, context=context)[0].pose_duree
        cr.execute("SELECT res_groups.id FROM res_groups WHERE res_groups.name='Groupe modification date de livraison'")
        res1 = cr.dictfetchone()
        id_group = res1 ['id']
        cr.execute("SELECT res_groups_users_rel.uid FROM res_groups_users_rel WHERE res_groups_users_rel.gid={0}".format(id_group))
        res2 = cr.fetchall()
        list_uid=[]
        value = {}
        for x in range(len(res2)):
            list_uid.append(res2[x][0])
        if uid in list_uid:
            value['test_groupe'] = True
        else:
            value['test_groupe'] = False
            value['pose_duree'] = duree_pose
        return {'value':value}
stock_picking()

class stock_picking_out(osv.osv):
    _inherit = "stock.picking.out"
    _columns = {
                'pose_duree': fields.float(string='Durée de la pose (jours)'),
                'test_groupe': fields.boolean(string='Est-ce dans le groupe'),
                }
    _defaults = {
                 'pose_duree':0.0,
                 'test_groupe':True,
                }
    
    def on_change_fields(self, cr, uid, ids, context=None):
        duree_pose = self.browse(cr, uid, ids, context=context)[0].pose_duree
        cr.execute("SELECT res_groups.id FROM res_groups WHERE res_groups.name='Groupe modification date de livraison'")
        res1 = cr.dictfetchone()
        id_group = res1 ['id']
        cr.execute("SELECT res_groups_users_rel.uid FROM res_groups_users_rel WHERE res_groups_users_rel.gid={0}".format(id_group))
        res2 = cr.fetchall()
        list_uid=[]
        value = {}
        for x in range(len(res2)):
            list_uid.append(res2[x][0])
        if uid in list_uid:
            value['test_groupe'] = True
        else:
            value['test_groupe'] = False
            value['pose_duree'] = duree_pose
        return {'value':value}
    
stock_picking_out()