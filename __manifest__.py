# -*- coding: utf-8 -*-
{
    'name': 'Automatización de Descuentos por Escalas Configurables',
    'version': '14.0.1.0.0',
    'category': 'Sales',
    'summary': 'Aplicar descuentos automáticos en facturas basados en historial de compras.',
    'author': 'Nelson Ivan Tontarelli',
    'website': 'https://github.com/NelsonIvan003',
    'depends': ['base', 'sale', 'account'],
    'data': [
        'views/eynes_descuento_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
