# -*- coding: utf-8 -*-
{
    'name': "Calculo de costos y precios",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Modulo que calcul el costo y precio de un nuevo producto
    """,

    'author': "Bleimar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','product','mrp'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/product_cost_view.xml',
        'views/product_template_view.xml',
        'views/material_cost_view.xml',
        'views/material_tools_service_cost_view.xml',
        'views/cutting_cost_view.xml',
        'views/operating_cost_view.xml',
    ],
}