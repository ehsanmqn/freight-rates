from datetime import date, datetime, timedelta

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from ratestask_port.models import Ports
from ratestask_price.models import Prices


class PricesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two ports
        Ports.objects.create(code='NYC00', name='New York City')
        Ports.objects.create(code='LAX00', name='Los Angeles')

        # Create a price object
        Prices.objects.create(
            orig_code=Ports.objects.get(code='NYC00'),
            dest_code=Ports.objects.get(code='LAX00'),
            day=date.today(),
            price=1000,
        )

    def test_orig_code_label(self):
        """
        Test verbose name of the orig_code label
        """
        price = Prices.objects.all()[0]
        field_label = price._meta.get_field('orig_code').verbose_name
        self.assertEqual(field_label, 'orig code')

    def test_dest_code_label(self):
        """
        Test verbose name of the dest_code label
        """
        price = Prices.objects.all()[0]
        field_label = price._meta.get_field('dest_code').verbose_name
        self.assertEqual(field_label, 'dest code')

    def test_day_label(self):
        """
        Test verbose name of the day label
        """
        price = Prices.objects.all()[0]
        field_label = price._meta.get_field('day').verbose_name
        self.assertEqual(field_label, 'day')

    def test_price_label(self):
        """
        Test verbose name of the price label
        """
        price = Prices.objects.all()[0]
        field_label = price._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')


class ListDailyAveragePriceV1TestCase(TestCase):
    """
    Test class for the ListDailyAveragePriceV1 view
    """

    def setUp(self):
        # create test data
        self.port1 = Ports.objects.create(code='NYC00', name='New York City')
        self.port2 = Ports.objects.create(code='LAX00', name='Los Angeles')
        self.price1 = Prices.objects.create(orig_code=self.port1, dest_code=self.port2,
                                            day=datetime.now().date() - timedelta(days=2), price=500)
        self.price2 = Prices.objects.create(orig_code=self.port1, dest_code=self.port2,
                                            day=datetime.now().date() - timedelta(days=1), price=600)
        self.price3 = Prices.objects.create(orig_code=self.port1, dest_code=self.port2,
                                            day=datetime.now().date(), price=700)

    def test_query_params_validation(self):
        """
        Test the serializer validation
        """
        url = reverse('list-daily-average-price-v1')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_from', response.data)
        self.assertIn('date_to', response.data)
        self.assertIn('origin', response.data)
        self.assertIn('destination', response.data)

    def test_list_daily_average_price(self):
        """
        Test the get_full_avg_daily_prices function
        """
        url = reverse('list-daily-average-price-v1')
        date_from = datetime.now().date() - timedelta(days=2)
        date_to = datetime.now().date()
        origin = 'CNSGH'
        destination = 'north_europe_main'

        response = self.client.get(url, {'date_from': date_from, 'date_to': date_to,
                                         'origin': origin, 'destination': destination})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['result']), 3)
        self.assertEqual(response.data['result'][0]['day'], str(date_from))
        self.assertEqual(response.data['result'][0]['average_price'], None)
        self.assertEqual(response.data['result'][1]['day'], str(date_from + timedelta(days=1)))
        self.assertEqual(response.data['result'][1]['average_price'], None)
        self.assertEqual(response.data['result'][2]['day'], str(date_from + timedelta(days=2)))
        self.assertEqual(response.data['result'][2]['average_price'], None)

    def test_list_contains_full_date(self):
        """
        Test the result contains full dates based on start and stop dates
        """
        url = reverse('list-daily-average-price-v1')
        date_from = datetime.now().date() - timedelta(days=32)
        date_to = datetime.now().date()
        origin = 'CNSGH'
        destination = 'north_europe_main'

        response = self.client.get(url, {'date_from': date_from, 'date_to': date_to,
                                         'origin': origin, 'destination': destination})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['result']), 33)

    def test_origin_null(self):
        """
        Test empty origin
        """
        url = reverse('list-daily-average-price-v1')
        date_from = datetime.now().date() - timedelta(days=32)
        date_to = datetime.now().date()
        origin = ''
        destination = 'north_europe_main'

        response = self.client.get(url, {'date_from': date_from, 'date_to': date_to,
                                         'origin': origin, 'destination': destination})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('origin', response.data)

    def test_origin_spaced(self):
        """
        Test spaced origin
        """
        url = reverse('list-daily-average-price-v1')
        date_from = datetime.now().date() - timedelta(days=32)
        date_to = datetime.now().date()
        origin = '     '
        destination = 'north_europe_main'

        response = self.client.get(url, {'date_from': date_from, 'date_to': date_to,
                                         'origin': origin, 'destination': destination})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('origin', response.data)