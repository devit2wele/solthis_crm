# -*- coding: utf-8 -*-
from odoo import models, _,fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
from datetime import date
from odoo import tools
from datetime import datetime
import logging
import threading
from array import *
import string
import random
import unicodedata


from dateutil import relativedelta
from workalendar.europe import France
cal = France()

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
SEXE=[
    ('M', 'M'),
    ('F', 'F'),
    ('C mixte', 'C mixte'),
    ('C M', 'C M'),
    ('C F', 'C F'),
    ('X indetermine', 'X indéterminé')
    ]
TYPE_PERSONNE=[
    ('Personne physique','Personne physique'),
    ('Personne morale','Personne morale'),
    ('Piege','Piège'),
    ('Anonyme','Anonyme'),
]
TITLE =[
    ('Monsieur', 'Monsieur'),
    ('Madame', 'Madame'),
    ('Mademoiselle', 'Mademoiselle'),
    ('M et Mme', 'M et Mme'),
	('M et M', 'M et M'),
    ('Mme et Mme', 'Mme et Mme'),
    ('Abbe', 'Abbe'),
]
STATUT =[
    ('Actif', 'Actif'),
    ('Doublon', 'Doublon'),
    ('Radie', 'Radie'),
    ('Ne pas prospecter', 'Ne pas prospecter'),
	('Decede', 'Décédé'),
]
CATEGORIE_ACTIF =[
    ('Mono Donateur', 'Mono Donateur'),
    ('Consolide', 'Consolidé'),
    ('Fidelise', 'Fidélisé'),
]
TAG =[
    ('oui', 'Oui'),
    ('non', 'Non'),
    ('peut-etre', 'Peut-être'),
]
STATUT_SOLL =[
    ('oui', 'Oui'),
    ('non', 'Non'),
    ('peut-etre', 'Peut-être'),
    ('en-cours', 'En cours'),
]
FREQ_COM=[
    ('Prospect','Prospect'),
    ('Nouveau','Nouveau'),
    ('Consolide','Consolidé'),
]
FREQ_DON=[
    ('0-6 mois','0-6 mois'),
    ('6-12 mois','6-12 mois'),
    ('12-18 mois','12-18 mois'),
    ('plus 18 mois', '+18 mois'),
]
DON_MOYEN=[
    ('1-50','1-50€'),
    ('50-250','50-250€'),
    ('250-500','250-500€'),
    ('500 et plus','500€ et plus'),
]
TYPE_HIST_COM=[
    ('Telemarketing','Télémarketing'),
    ('Email','Email'),
    ('Papier','Papier'),
    ('SMS','SMS'),
    ('Evenement','Evénement'),
    ('Fax','Fax'),
    ('Rendez-vous','Rendez-vous'),
]
CAT_GRAND_DONATEUR=[
    ('Middle','Middle'),
    ('Global leader','Global leader'),
    ('Investisseur / fondateur','Investisseur / fondateur'),
]
HIST_SORTANT=[
    ('telemarketing', 'Télémarketing'),
    ('email', 'Email'),
    ('papier', 'Papier'),
    ('sms', 'SMS'),
    ('evenement', 'Evénement'),
    ('fax', 'Fax'),
    ('rendez-vous', 'Rendez-vous'),
]
HIST_ENTRANT=[
    ('plainte', 'Plainte'),
    ('administratif', 'Administratif'),
    ('discussion', 'Discussion'),
    ('demande informations', 'Demande d\'informations'),
]
TYPE_ORGANISATION=[
    ('Entreprise', 'Entreprise'),
    ('Fondation', 'Fondation'),
    ('Asso', 'Asso'),
    ('Fonds dotation',  'Fonds dotation'),
    ('Ecoles', 'Ecoles'),
    ('Autres','Autres'),
]
RETOUR_COURIER=[
    ('0','0'),
    ('1','1'),
    ('2','2'),
    ('NPAI ','NPAI (3 retours)'),
]
TRAITEMENT_ADRESSE=[
    ('RNVP','RNVP'),
    ('Charade-Estocade','Charade-Estocade'),
    ('Autre','Autre'),
]
TYPE_ARRET=[
    ('Non sollicitable','Non sollicitable'),
    ('Sollicitable Don', 'Sollicitable Don'),
    ('Sollicitable PA','Sollicitable PA'),
]
RECENCE=[
    ('Actif','Actif'),
    ('Inactifs recents','Inactifs récents'),
    ('Inactifs','Inactifs'),
    ('Grands inactifs','Grands inactifs'),
]
MONTANT=[
    ('Donor','Donor'),
    ('Middle donor','Middle donor'),
    ('Global Leader','Global Leader'),
    ('Investisseur Fondateur','Investisseur / Fondateur'),
]
STATUT_LEGS=[
    ('interesse', 'interesse'),
    ('testataire', 'testataire'),
    ('dossier legs en cour', 'dossier legs en cour'),
]
OUINONVIDE=[
    ('Vide','Vide'),
    ('Oui','Oui'),
    ('Non','Non'),
]
RF=[
    ('regulier','Régulier'),
    ('annuel','Annuel'),
    ('non','Non'),
    ('recurrent','Récurrent '),
]
COURRIER=[
    ('0','0'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4', '4'),
    ('Tous','Tous'),
]
SENS_SOLL=[
    ('entrant','Entrant'),
    ('sortant','Sortant'),
]
CANAL=[
    ('courrier','Courrier'),
    ('telephone','téléphone'),
    ('email','email'),
    ('fax','fax'),
    ('SMS','SMS'),
    ('face a face','face à face'),
    ('evenement physique','événement (physique)'),
    ('rendez-vous','Rendez-vous'),
    ('reseaux sociaux','réseaux sociaux'),
    ('messagerie instantannee','messagerie instantannée'),
]
TYPE_CONTACT=[
    ('administratif','Administratif'),
    ('demande information','Demande information'),
    ('plainte','Plainte'),
    ('Discussion','Discussion'),
]
QUALIF=[
    ('positif','Positif'),
    ('negatif','Négatif')
]
STATUT_TRAIT=[
    ('Oui','Oui'),
    ('non','non'),
    ('en_cours','en cours'),
]
ADHERANT=[
    ('oui','Oui'),
    ('non','Non'),
    ('en_cours','en cours'),
]
TELEMARK=[
    ('non appele','Non appelé'),
    ('non-joint','Non-Joint'),
    ('joint non utile','Joint Non-Utile'),
    ('joint utile','Joint Utile'),
]
CANAL2=[
    ('courrier', 'courrier'),
    ('email', 'email'),
]
MOTIF_FIN_ENGAGEMENT = [
    ('decision_solthis', 'Décision Solthis'),
    ('upgrade', 'Upgrade'),
    ('downgrade', 'downgrade'),
    ('incidents_paiement', 'Incidents de paiement'),
    ('autres', 'Autres'),
]

PERIODICITE = [
    ('un_mois', '1 mois'),
    ('deux_mois', '2 mois'),
    ('trois_mois', '3 mois'),
    ('quatre_mois', '4 mois'),
    ('six_mois', '6 mois'),
    ('douze_mois', '12 mois'),
]

PERIODICITE_MOIS_EN_ENTIER = {
    'un_mois': 1,
    'deux_mois': 2,
    'trois_mois': 3,
    'quatre_mois': 4,
    'six_mois': 6,
    'douze_mois': 12,
}

STATUT_ENGAGEMENT = [
    ('actif', 'Actif'),
    ('suspendu_temporairement', 'Suspendu Temporairement'),
    ('inactif', 'Inactif'),
]

MOTIF_MODIFICATION = [
    ('erreur', 'Erreur'),
    ('modification', 'Modification'),
    
]

MOIS = {
    1: 'Janvier',
    2: 'Fevrier',
    3: 'Mars',
    4: 'Avril',
    5: 'Mai',
    6: 'Juin',
    7: 'Juillet',
    8: 'Aout',
    9: 'Septembre',
    10: 'Octobre',
    11: 'Novembre',
    12: 'Decembre',
}
CHER={
    'Monsieur':'Cher',
    'Madame':'Chère',
    'Mademoiselle':'Chère',
    'M et Mme':'Chère',
    'M et M':'Cher',
    'Abbe':'Cher',
}

class Donateur(models.Model):
    """
    Class Donateu.
    """
    _name = 'crm.alima.donateur'
    _inherit = ['mail.thread']
    _description = 'Donateur'
    
    #liste des champs de la classe
    title = fields.Selection(TITLE, string='Civilité')
    name = fields.Char(String="Code", compute='compute_name', store=True)
    lastname = fields.Char(String="Nom")
    firstname =fields.Char(String="Prenom")
    dateNaissance=fields.Date(string='Date de naissance', store=True)
    mois_annees=fields.Boolean(string='Date Naissance(Mois et Annees)', store=False)
    mois =fields.Integer(string='Mois', store=False)
    annee =fields.Integer(string='Annee', store=False)
    sexe=fields.Selection(SEXE, string="Sexe", store=False)
    type_de_personne=fields.Selection(TYPE_PERSONNE, string="Type de personne")
    partenaire=fields.Boolean(string="Partenaire", store=False)
    raison_sociale=fields.Char(string="Raison sociale", store=False)
    type_organisation=fields.Char(string="type d\'organisation", store=False)
    function= fields.Char(string='fonction', store=False)
    sec_activite=fields.Char(string='secteur d\'activité', store=False)
    complementnom=fields.Char(string='Adresse 1 - Libellé de la voie')
    complementadresse=fields.Char(string='Adresse 1 - Complément adresse')
    voie=fields.Char(string='Adresse 1 - N° de voie')
    codebis=fields.Char(string='Adresse 1 - Code bis')
    hammeau=fields.Char(string='Adresse 1 - Hammeau Lieu-dit')
    codepostale=fields.Char(string='Adresse 1 - Code postal', index=True)
    ville=fields.Char(string='Adresse 1 - Ville')
    country_id = fields.Char(string='Adresse 1 - Pays')
    complementnom2=fields.Char(string='Adresse 2 - Libellé de la voie', store=False)
    complementadresse2=fields.Char(string='Adresse 2 - Complément adresse', store=False)
    voie2=fields.Char(string='Adresse 2 - N° de voie', store=False)
    codebis2=fields.Char(string='Adresse 2 - Code bis', store=False)
    hammeau2=fields.Char(string='Adresse 2 - Hammeau Lieu-dit', store=False)
    codepostale2=fields.Char(string='Adresse 2 - Code postal', store=False)
    ville2=fields.Char(string='Adresse 2 - Ville', store=False)
    country_id2 = fields.Char(string='Adresse 2 - Pays', store=False)
    email = fields.Char(string='Email 1', index=True)
    email2 = fields.Char(string='Email 2')
    personal_fone=fields.Char(string='Téléphone personnel 1')
    personal_fone2=fields.Char(string='Téléphone personnel 2', store=False)
    mobile = fields.Char(string='Portable 1', store=False)
    mobile2 = fields.Char(string='Portable 2', store=False)
    phone = fields.Char(string='Téléphone professionnel', store=False)
    fax = fields.Char(string='Fax', store=False)
    statut=fields.Selection(STATUT, index=True, string='Statut')
    idcontact=fields.Many2one('crm.alima.donateur', string='ID contact de la fiche active', ondelete='restrict', store=False)
    retour_courier=fields.Selection(RETOUR_COURIER, string='retour courier')
    traitement_adresse=fields.Selection(TRAITEMENT_ADRESSE, string='Traitement adresse', store=False)
    Date_traitement_adresse=fields.Date(string='Date de traitement adresse', store=False)
    code_fiabilite_adresse = fields.Integer(string='code fiabilité adresse', store=False)
    statut_PA=fields.Boolean(string='statut PA', compute='_is_statut_PA', store=True)
    Type_arret_PA=fields.Selection(TYPE_ARRET, string='type d\'arret')
    recence=fields.Selection(RECENCE, string='Récence', compute='compute_recence', store=True)
    freq_communication=fields.Selection(FREQ_COM, index=True, string='Fréquence de communication', default='Prospect', store=False)
    montant=fields.Selection(MONTANT, string="Montant", default='Donor', store=True)
    code_media_origine=fields.Many2one('crm.alima.code.media', string='code media origine', ondelete='restrict')
    statuts_Legs=fields.Selection(STATUT_LEGS, string='Statuts Legs', store=False)
    grand_donateur_potentiel=fields.Selection(OUINONVIDE, string='Grand Donateur', index=True)
    reseau_alima=fields.Selection(OUINONVIDE, string='Réseau Solthis', store=False)
    prospect=fields.Selection(OUINONVIDE, string='Prospect', store=False)
    prospect_qulifie=fields.Selection(OUINONVIDE, string='Prospect qualifié', store=False)
    connexion = fields.Char(string='Connexion', store=False)
    sollicit_contat = fields.Char(string='Solliciteur du contrat', store=False)
    com_sollicit = fields.Text(string='Commentaires solliciteur')
    tag_com_devel=fields.Selection(TAG, index=True, string='Target Comité de developpement', store=False)
    statut_soll=fields.Selection(STATUT_SOLL, index=True, string='Statut sollicitation')
    rf=fields.Selection(RF, string='frequence envoie RF', store=False)
    canal_envoi=fields.Selection(CANAL2, string="canal")
    telemarketing =fields.Boolean(string='Télémarketing', store=False)
    email3 =fields.Boolean(string='Email', store=False)
    courrier=fields.Selection(COURRIER, string='Courrier (préférence de réception par an)')
    sms =fields.Boolean(string='SMS', store=False)
    evenement =fields.Boolean(string='Evénement', store=False)
    option_fax=fields.Boolean(string='FAX', store=False)
    option_CNIL =fields.Boolean(string='CNIL', store=False)
    echange_mail=fields.Boolean(string='Echange adresse email', store=False)
    comm_preference_contrat=fields.Text(string='Commentaires préférences de contact')
    contacts = fields.One2many('crm.alima.contacts', 'donateur', string='Contacts', store=False)
    scorelai = fields.One2many('crm.alima.score.lai', 'donateur', string='Score LAI', store=False)
    dons = fields.One2many('crm.alima.don', 'donateur', string='Listes de dons')
    engagements = fields.One2many('crm.alima.engagements', 'donateur', string='Engagements')
    datePremierDon=fields.Date(string="Date premier don")
    montantPremierDon=fields.Integer(string="montant premier don", store=False)
    codemediaPremierDon=fields.Many2one('crm.alima.code.media', string='code media premier don', ondelete='restrict', store=False)
    dateDernierDon=fields.Date(string="Date dernier don")
    montantDernierDon=fields.Integer(string="Montant dernier don")
    codemediaDernierDon=fields.Many2one('crm.alima.code.media', string='code media dernier don', ondelete='restrict', store=False)
    datePremierDonHPA=fields.Date(string="Date premier don HPA", store=False)
    montantPremierDonHPA=fields.Integer(string="montant premier don HPA", store=False)
    codemediaPremierDonHPA=fields.Many2one('crm.alima.code.media', string='code media premier don HPA', ondelete='restrict', store=False)
    dateDernierDonHPA=fields.Date(string="Date dernier don HPA", store=False)
    montantDernierDonHPA=fields.Integer(string="Montant dernier don HPA", store=False)
    codemediaDernierDonHPA=fields.Many2one('crm.alima.code.media', string='code media dernier don HPA', ondelete='restrict', store=False)
    nombreDons=fields.Integer(string="Le nombre de don")
    nombreDonsHPA=fields.Integer(string="Le nombre de don hors PA")
    cumulDonTotal=fields.Integer(string="cumul des dons total", store=False)
    cumulDonHPA=fields.Integer(string="cumul des dons hors PA", store=False)
    don_moy=fields.Float( string="montant Moyen", store=False)
    don_moyHPA=fields.Float( string="montant Moyen hors PA", store=False)
    adherant=fields.Selection(ADHERANT, string="adherant", store=False)
    datepremieradh=fields.Date(string="date premier adhésion", store=False)
    datedernieradh=fields.Date(string="date dernier adhésion", store=False)
    datefinadh=fields.Date(string="date fin adhésion", store=False)
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'crm.alima.donateur')], string='Attachments', store=False)
    attachment_number = fields.Integer(compute='_get_attachment_number', string="Number of Attachments", store=False)
    ancien_statut=fields.Char(string="ancien statut", store=False)
    idpremierdon=fields.Integer(string='idpremierdon', store=False)
    iddernierdon=fields.Integer(string='iddernierdon', store=False)
    idpremierdonHPA=fields.Integer(string='idpremierdonHPA', store=False)
    iddernierdonsHPA=fields.Integer(string='iddernierdonsHPA', store=False)
    nombredonsstat = fields.Integer(compute='_get_dons_number', string="nombre de dons en stat", store=False)
    id_bulletin = fields.Char(string='Id Bulletin')
    #image = fields.Binary(string="image")
    identifiant_donateur = fields.Char(string='Identifiant Donateur', store=True)
    date_from=fields.Date(store=False)
    date_to=fields.Date(store=False)

    datetime_import = fields.Datetime(readonly=True, string="Date Import")
    date = fields.Date( string='Date du don', related='dons.date', store=True)
    statut_engagement = fields.Selection( string='Statut d\'engagement', related='engagements.statut_engagement', store=True)
    montant_total_don = fields.Float(store=True, compute="compute_montant_total_don")

    newsletter = fields.Boolean(string='S’abonner à la newsletter')
    remerciement = fields.Boolean(string='Remerciement Envoyé')

    #liste des fonctions
    @api.depends('dons')
    def compute_montant_total_don(self):
        montant = 0.0
        for res in self:
            for don in res.dons:
                montant += don.montantEur
            res.montant_total_don = montant

    def compute_montant_entre_2_date(self):
        amount = 0.0
        amount_lettre = ""
        
        if self.date_from and self.date_to:
            date_from = datetime.strptime(self.date_from, '%Y-%m-%d').date()
            date_to = datetime.strptime(self.date_to, '%Y-%m-%d').date()
            all_don_2_date = self.env["crm.alima.don"].search([
                ('date', '>=', fields.Date.to_string(date_from)),
                ('date', '<=', fields.Date.to_string(date_to)),
                ('mode_versement', '=', 'avec prelevement'),
                ('donateur', '=', self.id),
            ])
            for don in all_don_2_date:
                amount += don.montantEur
            amount_lettre = self.env["crm.alima.don"].convNombre(int(amount))
            date = 'du ' + str(self.date_from) + ' au ' + str(self.date_to)
            don = all_don_2_date[0]
        return {
            'amount': amount,
            'amount_lettre': amount_lettre,
            'date': date,
            'don':don,
        }

    def current_day(self):
        return date.today().day
    def current_month(self):
        return MOIS[date.today().month]
    def current_year(self):
        return date.today().year
    def get_title(self,title):
        return CHER[title]

    def all_partenaire_disable(self):
        all_donateurs = self.env['crm.alima.donateur'].search([('partenaire', '=', True)])
        for donateur in all_donateurs:
            donateur.write({
                'partenaire':False,
            })
 
    @api.multi
    def _get_attachment_number(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'crm.alima.donateur'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count']) for res in read_group_res)
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)
    @api.multi
    def _get_dons_number(self):
        for record in self:
            record.nombredonsstat  = record.nombreDons
    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        action['search_view_id'] = (self.env.ref('crm_solthis.ir_attachment_view_search_inherit_crm_alima').id, )
        return action
    @api.multi
    def action_get_dons_form_views(self):
        action_context = {'donateur': [self.id,]}
        return {
                'name': 'crm.alima.don.form',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'crm.alima.don',
                'context': action_context,
                'type': 'ir.actions.act_window',
                'nodestroy': False,
                'target': 'current',
            }
    @api.multi
    def action_get_dons_tree_views(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "crm.alima.don",
            "views": [[False, "tree"], [False, "form"]],
            "name": "liste des dons",
            "search_view_id" : self.env.ref('crm_solthis.model_crm_alima_donateur').id,
        }

    @api.one
    def incremente_id(self, vals_id):
        res = self

        while res.id != vals_id:
            copy = res.copy()
            res.unlink()
            res = copy[0]
        
        return res

    def id_generator(self, size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @api.multi
    def write(self, vals):
        if 'firstname' in vals:
            vals['firstname'] = vals['firstname'].title()
        if 'lastname' in vals:
            vals['lastname'] = vals['lastname'].upper()
        return super(Donateur, self).write(vals)

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals['identifiant_donateur'] = self.id_generator()
        res= super(Donateur, self).create(vals)
        res.firstname = res.firstname.title() if res.firstname else False
        res.lastname = res.lastname.upper() if res.lastname else False
        res.identifiant_donateur = str(res.identifiant_donateur) + str(res.id)

        if 'id' in vals and res.id != vals['id']:
            res = res.incremente_id(vals['id'])
        res = res[0] if type(res) == list else res

        if not res.name:
            if res.email:
                res.name = res.email.replace(' ','')
            elif res.firstname and res.codepostale:
                res.name = res.lastname.replace(' ','')+""+res.firstname.strip().title()+""+res.codepostale.replace(' ','')
                res.name = res.name.replace('-','')
            elif res.codepostale:
                res.name = res.lastname.replace(' ','')+""+res.codepostale.replace(' ','')
                res.name = res.name.replace('-','')
            elif res.firstname:
                res.name = res.lastname.replace(' ','')+""+res.firstname.strip().title()
                res.name = res.name.replace('-','')
            else:
                res.name= res.lastname.replace(' ','')
                res.name = res.name.replace('-','')
            res.name = res.name
            # data = unicode(res.name,'utf-8')
            res.name = unicodedata.normalize('NFKD', res.name).encode('ASCII', 'ignore').replace(" ","")
        return res
        #creation
    @api.depends('firstname','lastname','codepostale','email')
    def compute_name(self):
        for res in self:
            if res.email:
                res.name = res.email.replace(' ','')
            elif res.firstname and res.codepostale:
                res.name = res.lastname.replace(' ','').upper()+""+res.firstname.strip().title()+""+res.codepostale.replace(' ','')
                res.name = res.name.replace('-','')
            elif res.codepostale:
                res.name = res.lastname.replace(' ','').upper()+""+res.codepostale.replace(' ','')
                res.name = res.name.replace('-','')
            elif res.firstname:
                res.name = res.lastname.replace(' ','').upper()+""+res.firstname.strip().title()
                res.name = res.name.replace('-','')
            else:
                res.name= res.lastname.replace(' ','').upper()
                res.name = res.name.replace('-','')
            res.name = res.name
            # data = unicode(res.name,'utf-8')
            res.name = unicodedata.normalize('NFKD', res.name).encode('ASCII', 'ignore').replace(" ","")
    @api.depends('dateDernierDon')
    def compute_recence(self):
        for rec in self:
            if rec.dateDernierDon:
                diff= datetime.strptime(fields.Date.today(), tools.DEFAULT_SERVER_DATE_FORMAT) - datetime.strptime(rec.dateDernierDon, tools.DEFAULT_SERVER_DATE_FORMAT)
                if diff.days < 365:
                    rec.recence='Actif'
                elif diff.days > 365 and diff.days < 730:
                    rec.recence='Inactifs recents'
                elif diff.days > 730 and diff.days < 1460:
                    rec.recence='Inactifs'
                elif diff.days > 1460:
                    rec.recence='Grands inactifs'
    @api.one
    @api.depends('engagements')
    def _is_statut_PA(self):
        self.statut_PA = False
        for eng in self.engagements:
            if eng.statut_engagement and eng.statut_engagement == 'actif':
                self.statut_PA = True
        
    def compute_date_don(self, datetime):
        if not cal.is_working_day(datetime):
            return self.compute_date_don(datetime + relativedelta.relativedelta(days=1))
        return datetime

    def date_a_prelever(self, date):
        try:
            return str(datetime.strptime(date,'%Y/%m/%d')).split(' ')[0]
        except:
            t=date.split('/')
            f=int(t[2])-1
            t[2]=str(f)
            return str(self.date_a_prelever('/'.join(t))).split(' ')[0]

    def sheduler_nombre_don(self):
        all_donateurs = self.env['crm.alima.donateur'].search([])
        for donateur in all_donateurs:
            donateur.nombreDons = len(donateur.dons)

    def update_identifiant_donateur(self):
        all_donateurs = self.env['crm.alima.donateur'].search([])
        for donateur in all_donateurs:
            donateur.write({
                'identifiant_donateur': self.id_generator() + str(donateur.id)
            })

    @api.multi
    def action_recu_fiscal_regulier_form_views(self):
        action_context = {'donateur': self.id}
        return {
            'name': 'crm.alima.recu.fiscal.regulier.template.form',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'crm.alima.recu.fiscal.regulier.template',
            'context': action_context,
            'type': 'ir.actions.act_window',
            'nodestroy': False,
            'target': 'new',
        }

    def correction_nom_prenom(self):
        all_donateurs = self.env['crm.alima.donateur'].search([])
        for donateur in all_donateurs:
            if donateur.lastname:
                donateur.write({
                    'lastname' : donateur.lastname.upper()
                })
            if donateur.firstname:
                donateur.write({
                    'firstname' : donateur.firstname.title()
                })
        
    def scheduler_credit_coop(self):
        """
        On récuperer tous les donateurs de la base
        Pour chaque donateur on verifie s'il à un engagement(credit coop) 
        pour lequel on doit déclencher la création d'un don
        Param de verification: statut d'engagement, le don correspondant via le code media de l'engagement,
        date prochaine prélévement, periodicité, mode de versement
        """
        raise UserError(_("Test in"))
        all_donateurs = self.env['crm.alima.donateur'].search([])
        for donateur in all_donateurs:
            if donateur.engagements and donateur.dons:
                for eng in donateur.engagements:
                    if eng.statut_engagement == 'actif' and eng.date_prochain_prelevement and datetime.strptime(eng.date_prochain_prelevement, '%Y-%m-%d') < datetime.today():
                        for don in donateur.dons:
                            if don.codeMedia.id == eng.code_media.id and don.moyen_paiment == 'Compte bancaire' and don.mode_versement=="avec prelevement":
                                #Creation du don credit coop
                                date_du_don = self.compute_date_don(datetime.strptime(eng.date_prochain_prelevement, '%Y-%m-%d'))
                                create_don = self \
                                    .env['crm.alima.don'] \
                                    .search([('donateur', '=', donateur.id),('codeMedia', '=', eng.code_media.id)], limit=1) \
                                    .copy({
                                        'date': str(date_du_don),
                                        'montantEur': eng.montant,
                                })

                                #Mise à jour de l'engagement aprés la création du don
                                if create_don:
                                    if eng.date_premier_prelevement:
                                        jour = eng.date_premier_prelevement.split('-')[2]
                                        date = create_don.date.split('-')
                                        date[2] = jour
                                        date = "/".join(date)
                                        date_prochain = self.date_a_prelever(date)
                                    else:
                                        date_prochain = create_don.date

                                    eng.write({
                                        'date_dernier_prelevement': create_don.date,
                                        'date_prochain_prelevement': str(self.compute_date_don(
                                            datetime.strptime(date_prochain,'%Y-%m-%d')     
                                                +
                                            relativedelta.relativedelta(months=PERIODICITE_MOIS_EN_ENTIER[eng.periodicite])
                                        )) 

                                    })
                                #Le premier don qu'on rencontre qui vient de credit coop. 
                                #On incremente d'un don puis on sort de la boucle
                                break


class ScoreLAI(models.Model):
    _name = 'crm.alima.score.lai'
    _description = 'SCORE LAI'

    """
    SCORE LAI: creation d'une table pour l'historique
    """
    #liste des champs de la classe
    linkage =fields.Integer(string='Linkage')
    ability =fields.Integer(string='Ability')
    interest =fields.Integer(string='Interest')
    score_LAI = fields.Integer(compute='compute_LAI', store=True)
    date_debut=fields.Date(string="Date")
    commentaires_LAI =fields.Text(string='Commentaires LAI')
    donateur = fields.Many2one('crm.alima.donateur', string='donateur', required=True)

    @api.depends('linkage', 'ability','interest')
    def compute_LAI(self):
        for rec in self:
            rec.score_LAI = rec.linkage + rec.ability + rec.interest
    _sql_constraints = [
        ('check_linkage', "check (linkage <= 5)",
            "La valeur de linkage doit etre inferieur à 5"),
        ('check_ability', "check (ability <= 5)",
            "La valeur de ability doivent etre inferieur à 5"),
        ('check_interest', "check (interest <= 5)",
            "La valeur de interest doit etre inferieur à 5"),
    ]

class Contacts(models.Model):
    _name = 'crm.alima.contacts'
    _description = 'Contacts'

    code_media=fields.Many2one('crm.alima.code.media', string='code media', ondelete='restrict', store=False)
    libelle=fields.Char(string='libellé')
    date=fields.Date(string='Date')
    sens_solliciteur=fields.Selection(SENS_SOLL, string='Sens')
    canal=fields.Selection(CANAL, string='canal', store=False)
    type_contact=fields.Selection(TYPE_CONTACT, string='Type de contact')
    contenu=fields.Char(string='Contenu')
    qualif=fields.Selection(QUALIF, string='Qualificatif')
    theme=fields.Char(string='Thème')
    statut_trait=fields.Selection(STATUT_TRAIT, string='Statut traitement')
    date_traitement=fields.Date(string='Date de traitement')
    resp_traitement=fields.Many2one('res.users', string='Responsable traitement')
    org_traitement=fields.Char(string='Organisme dans le cas d\'un échange de contact')
    date_retour_telemark=fields.Date(string='date retour télémarketing')
    code_retour_telemark=fields.Date(string='code média retour télémarketing')
    statut_telemark=fields.Selection(TELEMARK, string='retour tele')
    donateur = fields.Many2one('crm.alima.donateur', string='donateur', required=True)

    #liste des fonctions
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        res= super(Contacts, self).create(vals)
        #rec = res.donateur
        return res

class Engagement(models.Model):
    _name = 'crm.alima.engagements'
    _description = 'Engagements'

    donateur = fields.Many2one('crm.alima.donateur', string='donateur', required=True)
    code_media_origine = fields.Many2one('crm.alima.code.media', string='code media origine', ondelete='restrict', store=False)
    code_media = fields.Many2one('crm.alima.code.media', string='code media', ondelete='restrict')
    
    date_accord_mandat = fields.Date(string='Date d\'accord du mandat')
    date_engagement_mandat = fields.Date(string='Date d\'engagement du mandat')
    date_fin_mandat = fields.Date(string='Date de fin du mandat')
    date_fin_engagement = fields.Date(string='Date fin engagement')
    motif_fin_engagement = fields.Selection(MOTIF_FIN_ENGAGEMENT, string='Motif fin d\'engagement', store=False)
    code_media_engagement_modifie = fields.Many2one('crm.alima.code.media', string='code media engagement modifié', ondelete='restrict')
    montant = fields.Float(string="Montant")
    periodicite = fields.Selection(PERIODICITE, string='Periodicité')
    statut_engagement = fields.Selection(STATUT_ENGAGEMENT, string='Statut d\'engagement')
    date_premier_prelevement = fields.Date(string='Date premier prélèvement')
    date_dernier_prelevement = fields.Date(string='Date dernier prélèvement')
    montant_supplementaire_prochain_prelevement = fields.Float(string='Montant supplémentaire exceptionnel du prochain prélèvement', store=False)
    date_prochain_prelevement = fields.Date(string='Date prochain prélèvement')
    nom_banque = fields.Char(string='Nom banque')
    numero_iban = fields.Char(string='Numéro IBAN')
    code_bic = fields.Char(string='Code BIC')
    code_identifiant_debiteur = fields.Char(string='Code identifiant débiteur')
    reference_unique_mandat = fields.Char(string='Référence unique de mandat')
    identifiant_cb = fields.Char(string='Identifiant CB')
    date_expiration_cb = fields.Char(string='Date d\'expiration CB')
    remarques = fields.Char(string='Remarques', store=False)
    motif_modification = fields.Selection(MOTIF_MODIFICATION, string="Motif modification", store=False)
    lastname = fields.Char( string='Nom Donateur', related='donateur.lastname', store=True)
    firstname = fields.Char( string='Prénom Donateur', related='donateur.firstname', store=True)
    id_matricule = fields.Integer(string='Id Matricule')
    datetime_import = fields.Datetime(readonly=True, string="Date Import")

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals): 
        vals['code_media_origine'] = vals['code_media']
        
        return super(Engagement, self).create(vals)


    @api.multi
    def write(self, vals):
        res = self

        if u'motif_modification' not in vals:
            #Pour la création d'un engagement
            rep  =  super(Engagement, self).write(vals)
        
        elif vals[u'motif_modification'] in [False, u'erreur'] or res.statut_engagement in [False, 'inactif']:    
            #Pour la correction de saisi d'un engagement
            rep  =  super(Engagement, self).write(vals)
        
        else:
            #creation d'un nouvel engagement avec les même info que l'engagement dérivé
            new_eng = super(Engagement, self).create({
                'donateur': res.donateur.id,
                'code_media': res.code_media.id,
                'code_media_origine': res.code_media_origine.id,
                'date_accord_mandat' : res.date_accord_mandat,
                'date_engagement_mandat' : res.date_engagement_mandat,
                'date_fin_mandat' : res.date_fin_mandat,
                'date_fin_engagement' : res.date_fin_engagement,
                'motif_fin_engagement' : res.motif_fin_engagement,
                'code_media_engagement_modifie' : res.code_media.id, 
                'montant' : res.montant,
                'periodicite' : res.periodicite,
                'statut_engagement' : res.statut_engagement,
                'date_premier_prelevement' : res.date_premier_prelevement,
                'date_dernier_prelevement' : res.date_dernier_prelevement,
                'montant_supplementaire_prochain_prelevement' : res.montant_supplementaire_prochain_prelevement,
                'date_prochain_prelevement' : res.date_prochain_prelevement,
                'nom_banque' : res.nom_banque,
                'numero_iban' : res.numero_iban,
                'code_bic' : res.code_bic,
                'code_identifiant_debiteur' : res.code_identifiant_debiteur,
                'reference_unique_mandat' : res.reference_unique_mandat,
                'identifiant_cb' : res.identifiant_cb,
                'date_expiration_cb': res.date_expiration_cb,
                'remarques' : res.remarques,  
            })
            vals[u'motif_modification'] = False # Pour sortir de la boucle
            new_eng.write(vals)

            #desactivation de l'engagement
            rep  =  super(Engagement, self).write({
                'statut_engagement' : 'inactif',
            })


        return rep

    @api.model
    def default_get(self, fields):    
        res = super(Engagement, self).default_get(fields)        
        if 'nom_banque' in fields:        
            res.update({
                'statut_engagement' : 'actif',

            })    
        return res

    @api.multi
    def unlink(self):
        res = super(Engagement, self).unlink()
        return { 'type': 'ir.actions.client', 'tag': 'reload', }

