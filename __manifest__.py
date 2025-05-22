{
    'name': 'Travel Management',

    'description': 'Travel Expenses Management Module',

    'summary': 'Travel Expenses Management Module',

    'license': 'LGPL-3',

    'data': [
            'security/ir.model.access.csv',
            
            'views/travel_mgmt_views.xml',
            'views/travel_mgmt_line_views.xml',
            'views/travel_mgmt_menu_views.xml'
        ],

    'depends': [
        'hr_expense',
    ]

}