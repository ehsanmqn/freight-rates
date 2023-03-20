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