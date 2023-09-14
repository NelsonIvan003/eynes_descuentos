from odoo import models, fields, api


class EynesDescuento(models.Model):
    _name = 'eynes.descuento'
    _description = 'Descuentos configurables por escalas'

    name = fields.Char(string='Nombre', required=True)
    rango_min = fields.Float(string='Rango Mínimo', required=True)
    rango_max = fields.Float(string='Rango Máximo', required=True)
    descuento = fields.Float(string='(%) Descuento', required=True)

    # config_settings_id = fields.Many2one('res.config.settings', string='Configuración Principal')

    _sql_constraints = [
        ('range_overlap', 'CHECK(rango_min <= rango_max)', 'Los rangos no pueden solaparse.'),
        ('discount_range', 'CHECK(descuento >= 0 AND descuento <= 100)', 'El descuento debe estar entre 0% y 100%.'),
    ]
