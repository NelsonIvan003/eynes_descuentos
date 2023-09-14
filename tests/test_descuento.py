from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestInvoiceDiscount(TransactionCase):
    def setUp(self):
        super(TestInvoiceDiscount, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'Cliente de Prueba'})

    def test_aplicar_descuento(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'amount_total': 1000.00,
        })

        invoice.aplicar_descuento()

        self.assertEqual(invoice.amount_total, 800.00, "El descuento no se aplicó correctamente.")
