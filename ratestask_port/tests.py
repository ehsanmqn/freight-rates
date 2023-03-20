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

    def test_port_fields(self):
        """
        Test that object created according to what specified in the task description
        """
        port = Ports.objects.get(code='TCODE')
        self.assertEqual(port.code, 'TCODE')
        self.assertEqual(port.name, 'Test Port')
        self.assertEqual(port.parent_slug, self.region)

    def test_str_method(self):
        """
        Test that the __str__ method returns the port code correctly
        """
        port = Ports.objects.get(code="TCODE")
        self.assertEqual(str(port), "TCODE")

    def test_unique_code(self):
        """
        Test whether the code field is unique
        """
        with self.assertRaises(Exception):
            Ports.objects.create(
                code="TCODE",
                name="Test Port",
                parent_slug=Regions.objects.create(
                    slug="test_region",
                    name="Test Region"
                )
            )

    def test_code_max_length(self):
        """
        Test that the code field has the correct max length
        """
        with self.assertRaises(Exception):
            Ports.objects.create(
                code="TCODE" * 10,
                name="Test Port",
                parent_slug=Regions.objects.create(
                    slug="test_region",
                    name="Test Region"
                )
            )

    def test_name_max_length(self):
        """
        Test that the name field has the correct max length
        """
        with self.assertRaises(Exception):
            Ports.objects.create(
                code="TCODE" * 20,
                name="Test Port",
                parent_slug=Regions.objects.create(
                    slug="test_region",
                    name="Test Region"
                )
            )

    def test_parent_slug_null(self):
        """
        Test that the parent_slug field can be null
        """
        port = Ports.objects.create(
            code="TCOD2",
            name="Test Port2"
        )
        self.assertIsNone(port.parent_slug)