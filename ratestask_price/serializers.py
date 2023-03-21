from datetime import timedelta, datetime

from rest_framework import serializers

from ratestask_port.models import Ports


class ListDailyAveragePriceInputSerializerV1(serializers.Serializer):
    """
    Input serializer class for the ListDailyAveragePriceV1 view class with validation on origin and destination
    """
    date_from = serializers.DateField(required=True, allow_null=False)
    date_to = serializers.DateField(required=True, allow_null=False)
    origin = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    destination = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def validate_date_to(self, value):
        if value >= datetime.now().date() + timedelta(days=365*5):
            raise serializers.ValidationError("Too big date to parameter.")
        return value

    def validate_date_from(self, value):
        if value <= datetime.now().date() - timedelta(days=365*5):
            raise serializers.ValidationError("Too small date from parameter.")
        return value

    def validate_origin(self, value):
        origin = Ports.get_ports_by_code_or_slug(value=value)

        if len(origin) == 0:
            raise serializers.ValidationError("Invalid origin port symbol.")
        return origin

    def validate_destination(self, value):
        destination = Ports.get_ports_by_code_or_slug(value=value)

        if len(destination) == 0:
            raise serializers.ValidationError("Invalid destination port symbol.")
        return destination


class ListDailyAveragePriceInputSerializerV2(serializers.Serializer):
    """
    Input serializer class for the ListDailyAveragePriceV2 view class
    """
    date_from = serializers.DateField(required=True, allow_null=False)
    date_to = serializers.DateField(required=True, allow_null=False)
    origin = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    destination = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def validate_date_to(self, value):
        if value >= datetime.now().date() + timedelta(days=365*5):
            raise serializers.ValidationError("Too big date to parameter.")
        return value

    def validate_date_from(self, value):
        if value <= datetime.now().date() - timedelta(days=365*5):
            raise serializers.ValidationError("Too small date from parameter.")
        return value


class ListDailyAveragePriceOutputSerializer(serializers.Serializer):
    """
    Output serializer class for the ListDailyAveragePrice view
    """
    day = serializers.DateField()
    average_price = serializers.IntegerField()
