{
    'name': "Scrap Return IUH",

    'summary': """
         Scrap Return IUH""",

    'description': """
        Scrap Return IUH.
    """,

    'author': "Group 56",
    'website': "",
    'license': 'OPL-1',
    'category': 'Others',
    'version': '14.0.1',
    'depends': ['stock','iuh_stock'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        # 'views/menu.xml',
        'views/product_quality_view.xml',
        'views/stock_lot_view.xml'

    ],

}