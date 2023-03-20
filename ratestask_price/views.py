from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ratestask_price.serializers import ListDailyAveragePriceInputSerializer


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

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": []
        }, status=status.HTTP_200_OK)
