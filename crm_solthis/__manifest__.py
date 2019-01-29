# -*- coding: utf-8 -*-
{
    'name': 'crm donateur',
    'version': '1.0',
    'category': 'CRM',
    'description': 'CRM Donateur',
    'depends': [
        'base',
        'mail',
        'document',
        #'report',
    ],
    'author': 'Elimane NDOME, Aliou Samba WELE, IT4LIFE',
    'website': 'solthis-ngo.org',
    'license': 'AGPL-3',
    'data': [
        'views/import_don_credit_coop.xml',
        'views/import_donateur_credit_coop.xml',
        'views/import_engagement.xml',
        'views/update_don.xml',
        'views/engagements_view.xml',
        'views/donateur_view.xml',
        'views/dons_view.xml',
        'views/code_media_view.xml',
        'views/menu_view.xml',
        #'wizard/crm_alima_recu_fiscal_regulier.xml',
        #'report/style.xml',
        #'report/crm_alima_report_views.xml',
        #'report/crm_alima_report.xml',
        #'report/recu_fiscal_ponctuel.xml',
        #'report/recu_fiscal_regulier.xml',
        #'data/mail_template_data.xml',
        'security/collecte_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
}
