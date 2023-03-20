from django.test import TestCase

from ratestask_port.models import Ports
from ratestask_region.models import Regions


class PortsModelTestCase(TestCase):
    """
    Test class for the Ports model
    """

    def setUp(self):
        self.region = Regions.objects.create(
            slug='test_region',
            name='Test Region'
        )

        self.port = Ports.objects.create(
            code='TCODE',
            name='Test Port',
            parent_slug=self.region
        )

    def test_port_creation(self):
        """
        Test whether port create properly
        """
        port = self.port
        self.assertTrue(isinstance(port, Ports))
        self.assertEqual(port.__str__(), port.code)
