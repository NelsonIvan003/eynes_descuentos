from odoo import models, fields, api, exceptions
from datetime import date, timedelta, datetime


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_rango_dias_mes_anterior(self):
        hoy = datetime.now()
        primer_dia_mes_en_curso = hoy.replace(day=1)
        ultimo_dia_mes_anterior = primer_dia_mes_en_curso - timedelta(days=1)
        primer_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)
        return primer_dia_mes_anterior, ultimo_dia_mes_anterior

    def get_total_gastos_cliente_mes_anterior(self, customer_id):
        primer_dia, ultimo_dia = self.get_rango_dias_mes_anterior()
        # ventas
        invoices = self.env['account.move'].search([
            ('partner_id', '=', customer_id),
            ('date', '>=', primer_dia),
            ('date', '<=', ultimo_dia),
            ('move_type', '=', 'out_invoice'),
        ])
        # notas de crédito de las ventas
        credit_notes = self.env['account.move'].search([
            ('partner_id', '=', customer_id),
            ('date', '>=', primer_dia),
            ('date', '<=', ultimo_dia),
            ('move_type', '=', 'out_refund')
        ])
        total_gastos = sum(invoices.mapped('amount_total')) - sum(credit_notes.mapped('amount_total'))
        return total_gastos

    def aplicar_descuento(self):
        for invoice in self:
            if invoice.move_type == 'out_invoice':  # facturas de ventas
                customer_id = invoice.partner_id.id
                total_factura_antes_descuento = invoice.amount_total  # Guardar el total antes del descuento
                total_gastos_mes_pasado = self.get_total_gastos_cliente_mes_anterior(customer_id)
                descuento = self.env['eynes.descuento'].search([
                    ('rango_min', '<=', total_gastos_mes_pasado),
                    ('rango_max', '>=', total_gastos_mes_pasado),
                ])
                if descuento:
                    max_discount = max(descuento.mapped('descuento'))
                    invoice.amount_total *= (1 - (max_discount / 100))



    @api.model
    def create(self, vals):
        invoice = super(AccountMove, self).create(vals)
        invoice.aplicar_descuento()  # Aplicar el descuento al crear la factura
        return invoice

