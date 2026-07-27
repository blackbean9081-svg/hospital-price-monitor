from rest_framework import serializers

from .models import Hospital, TreatmentPrice


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'region']


class TreatmentPriceSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = TreatmentPrice
        fields = ['id', 'hospital', 'hospital_name', 'treatment_name', 'listed_price', 'guaranteed_price']
