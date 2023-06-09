import datetime

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ratestask_price.models import Prices
from ratestask_price.responses import send_http_response
from ratestask_price.serializers import ListDailyAveragePriceInputSerializerV1, ListDailyAveragePriceOutputSerializer, \
    ListDailyAveragePriceInputSerializerV2


class ListDailyAveragePriceV1(APIView):
    """
    List daily average price between two defined date for given ports or regions

    Query parameters
    date_from: Starting date in YYYY-MM-DD format
    date_to: End date in YYYY-MM-DD format
    origin: Origin port code or region slug
    destination: Destination port code or region slug
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ListDailyAveragePriceInputSerializerV1

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        origin = data.get('origin')
        destination = data.get('destination')

        # Check whether dates well-sequenced
        if date_to < date_from:
            return send_http_response(code=status.HTTP_400_BAD_REQUEST,
                                      message="The sequencing of dates is incorrect.")

        # Limit the time range to 2 years
        if abs(date_to - date_from) > datetime.timedelta(365 * 2):
            return send_http_response(code=status.HTTP_400_BAD_REQUEST,
                                      message="Too broad dates range (MAX: 2 years).")

        # Bundle port codes as a tuple to feed them to the query
        origins = tuple([item[0] for item in origin])
        destins = tuple([item[0] for item in destination])

        try:
            # Query for getting average prices per day
            queryset = Prices.get_avg_daily_prices_v1(origins=origins, destins=destins,
                                                      date_from=date_from, date_to=date_to)
        except Exception as e:
            return send_http_response(code=status.HTTP_417_EXPECTATION_FAILED,
                                      message="Operation failed.")

        # Serialize output data
        serialized_data = ListDailyAveragePriceOutputSerializer(queryset, many=True,
                                                                context={"request": request}).data

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": serialized_data
        }, status=status.HTTP_200_OK)


class ListDailyAveragePriceV2(APIView):
    """
    List daily average price between two defined date for given ports or regions
    This is the second version of the same API, but it uses a different query structure

    Query parameters
    date_from: Starting date in YYYY-MM-DD format
    date_to: End date in YYYY-MM-DD format
    origin: Origin port code or region slug
    destination: Destination port code or region slug
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ListDailyAveragePriceInputSerializerV2

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        origin = data.get('origin')
        destination = data.get('destination')

        # Check whether dates well-sequenced
        if date_to < date_from:
            return send_http_response(code=status.HTTP_400_BAD_REQUEST,
                                      message="The sequencing of dates is incorrect.")

        # Limit the time range to 2 years
        if abs(date_to - date_from) > datetime.timedelta(365 * 2):
            return send_http_response(code=status.HTTP_400_BAD_REQUEST,
                                      message="Too broad dates range (MAX: 2 years).")

        try:
            # Query for getting average prices per day
            queryset = Prices.get_avg_daily_prices_v2(origins=origin, destins=destination,
                                                      date_from=date_from, date_to=date_to)
        except Exception as e:
            return send_http_response(code=status.HTTP_417_EXPECTATION_FAILED,
                                      message="Operation failed.")

        # Serialize output data
        serialized_data = ListDailyAveragePriceOutputSerializer(queryset, many=True,
                                                                context={"request": request}).data

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": serialized_data
        }, status=status.HTTP_200_OK)
