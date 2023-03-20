from rest_framework import serializers


class ListDailyAveragePriceInputSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=True, allow_null=False)
    date_to = serializers.DateField(required=True, allow_null=False)
    origin = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    destination = serializers.CharField(required=True, allow_blank=False, allow_null=False)
