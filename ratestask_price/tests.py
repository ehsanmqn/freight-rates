from datetime import date

from django.test import TestCase

from ratestask_port.models import Ports
from ratestask_price.models import Prices


class PricesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two ports
        Ports.objects.create(port_code='NYC00', port_name='New York City')
        Ports.objects.create(port_code='LAX00', port_name='Los Angeles')

        # Create a price object
        Prices.objects.create(
            orig_code=Ports.objects.get(port_code='NYC00'),
            dest_code=Ports.objects.get(port_code='LAX00'),
            day=date.today(),
            price=1000,
        )

    def test_orig_code_label(self):
        """
        Test verbose name of the orig_code label
        """
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('orig_code').verbose_name
        self.assertEqual(field_label, 'orig code')

    def test_dest_code_label(self):
        """
        Test verbose name of the dest_code label
        """
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('dest_code').verbose_name
        self.assertEqual(field_label, 'dest code')

    def test_day_label(self):
        """
        Test verbose name of the day label
        """
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('day').verbose_name
        self.assertEqual(field_label, 'day')

    def test_price_label(self):
        """
        Test verbose name of the price label
        """
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')