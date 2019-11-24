from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from interviewapp.models import Interview


class InterviewSerializer(ModelSerializer):
    slot = serializers.SerializerMethodField()

    @staticmethod
    def get_slot(obj):
        return obj.get_slot_display()

    class Meta:
        model = Interview
        fields = '__all__'