from django.test import TestCase

from ratestask_region.models import Regions


class RegionsTestCase(TestCase):
    """
    Test class for the Regions model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for all class methods. This runs only once.
        """
        Regions.objects.create(
            slug="europe",
            name="Europe"
        )

    def test_str_method(self):
        """
        Test that the __str__ method returns the slug of the region correctly
        """
        region = Regions.objects.get(slug="europe")
        self.assertEqual(str(region), "europe")
