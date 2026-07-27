from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TreatmentPrice(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='treatment_prices')
    treatment_name = models.CharField(max_length=100)
    listed_price = models.IntegerField()
    guaranteed_price = models.IntegerField()

    def __str__(self):
        return f'{self.hospital.name} - {self.treatment_name}'
