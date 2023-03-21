from rest_framework import serializers

from ratestask_port.models import Ports
from ratestask_price.validators import validate_origin_destination


class ListDailyAveragePriceInputSerializerV1(serializers.Serializer):
    """
    Input serializer class for the ListDailyAveragePriceV1 view class with validation on origin and destination
    """
    date_from = serializers.DateField(required=True, allow_null=False)
    date_to = serializers.DateField(required=True, allow_null=False)
    origin = serializers.CharField(required=True, allow_blank=False, allow_null=False,
                                   validators=[validate_origin_destination])
    destination = serializers.CharField(required=True, allow_blank=False, allow_null=False,
                                        validators=[validate_origin_destination])


class ListDailyAveragePriceInputSerializerV2(serializers.Serializer):
    """
    Input serializer class for the ListDailyAveragePriceV2 view class
    """
    date_from = serializers.DateField(required=True, allow_null=False)
    date_to = serializers.DateField(required=True, allow_null=False)
    origin = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    destination = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class ListDailyAveragePriceOutputSerializer(serializers.Serializer):
    """
    Output serializer class for the ListDailyAveragePrice view
    """
    day = serializers.DateField()
    average_price = serializers.IntegerField()
