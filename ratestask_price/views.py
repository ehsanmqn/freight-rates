from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ratestask_price.models import Prices
from ratestask_price.serializers import ListDailyAveragePriceInputSerializer, ListDailyAveragePriceOutputSerializer


class ListDailyAveragePrice(APIView):
    """
    List daily average price between two defined date for given ports or regions
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ListDailyAveragePriceInputSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        origin = data.get('origin')
        destination = data.get('destination')

        print(">>>> ", date_from, date_to, origin, destination)

        origins = tuple([item[0] for item in origin])
        destins = tuple([item[0] for item in destination])

        queryset = Prices.get_avg_daily_prices(origins=origins, destins=destins,
                                               date_from=date_from, date_to=date_to)

        serialized_data = ListDailyAveragePriceOutputSerializer(queryset, many=True,
                                                                context={"request": request}).data

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": serialized_data
        }, status=status.HTTP_200_OK)
