from rest_framework import serializers


class BadRequestResponseSerializer(serializers.Serializer):
    errors = serializers.DictField()


class CommonErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    status_code = serializers.IntegerField()
    error = serializers.CharField()
