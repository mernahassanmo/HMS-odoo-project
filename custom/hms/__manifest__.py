{
    'name': 'hms_patient',
    'summary': 'hospital management system',
    'depends': ['base', 'crm'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
        'views/hms_log_history_views.xml',
        'views/crm_customer_views.xml',
        'reports/report.xml',
        'reports/template.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
