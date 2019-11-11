# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    largeur = fields.Float(
        string='Largeur',
    )
    hauteur = fields.Float(
        string='Hauteur',
    )
    dimension = fields.Float(
        string='Dimension',
    )
    vitre = fields.Many2one(
        'mim.article',
        string='Vitre',
    )
    type_vitre = fields.Selection(
        [('simple','Simple'),
         ('double','Double')], 
        string="",
    )
    decoratif = fields.Many2one(
        'mim.article',
        string='Décoratif',
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
         ('inegaux','Inégaux')], 
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
        'Nombre division'
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
        [('sans','Sans intermédiaire'),
         ('avec','Avec intermédiaire')], 
        string="Intermédiaire"
    )