from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ratestask_price.models import Prices
from ratestask_price.serializers import ListDailyAveragePriceInputSerializerV1, ListDailyAveragePriceOutputSerializer, \
    ListDailyAveragePriceInputSerializerV2


class ListDailyAveragePriceV1(APIView):
    """
    List daily average price between two defined date for given ports or regions
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

        # Bundle port codes as a tuple to feed them to the query
        origins = tuple([item[0] for item in origin])
        destins = tuple([item[0] for item in destination])

        try:
            # Query for getting average prices per day
            queryset = Prices.get_avg_daily_prices_v1(origins=origins, destins=destins,
                                                      date_from=date_from, date_to=date_to)
        except Exception as e:
            return Response({
                "code": status.HTTP_417_EXPECTATION_FAILED,
                "message": "Operation failed: " + str(e),
                "result": []
            }, status=status.HTTP_417_EXPECTATION_FAILED)

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

        try:
            # Query for getting average prices per day
            queryset = Prices.get_avg_daily_prices_v2(origins=origin, destins=destination,
                                                      date_from=date_from, date_to=date_to)
        except Exception as e:
            return Response({
                "code": status.HTTP_417_EXPECTATION_FAILED,
                "message": "Operation failed: " + str(e),
                "result": []
            }, status=status.HTTP_417_EXPECTATION_FAILED)

        # Serialize output data
        serialized_data = ListDailyAveragePriceOutputSerializer(queryset, many=True,
                                                                context={"request": request}).data

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": serialized_data
        }, status=status.HTTP_200_OK)