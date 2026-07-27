from django.db.models import F
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Hospital, TreatmentPrice
from .serializers import HospitalSerializer, TreatmentPriceSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class TreatmentPriceViewSet(viewsets.ModelViewSet):
    queryset = TreatmentPrice.objects.select_related('hospital').all()
    serializer_class = TreatmentPriceSerializer


@api_view(['GET'])
def compare_prices(request):
    treatment = request.query_params.get('treatment', '').strip()
    if not treatment:
        return Response(
            {'error': 'treatment 쿼리 파라미터가 필요합니다. 예: /api/compare/?treatment=라식'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    prices = (
        TreatmentPrice.objects.select_related('hospital')
        .filter(treatment_name=treatment)
        .order_by('listed_price')
    )

    if not prices:
        return Response({'treatment': treatment, 'count': 0, 'lowest_price': None, 'results': []})

    lowest_price = prices[0].listed_price
    results = [
        {
            'hospital': p.hospital.name,
            'region': p.hospital.region,
            'treatment_name': p.treatment_name,
            'listed_price': p.listed_price,
            'guaranteed_price': p.guaranteed_price,
            'is_lowest': p.listed_price == lowest_price,
        }
        for p in prices
    ]
    return Response({
        'treatment': treatment,
        'count': len(results),
        'lowest_price': lowest_price,
        'results': results,
    })


@api_view(['GET'])
def monitor_prices(request):
    violations = (
        TreatmentPrice.objects.select_related('hospital')
        .filter(listed_price__gt=F('guaranteed_price'))
        .order_by('-listed_price')
    )

    results = [
        {
            'hospital': p.hospital.name,
            'treatment_name': p.treatment_name,
            'listed_price': p.listed_price,
            'guaranteed_price': p.guaranteed_price,
            'excess': p.listed_price - p.guaranteed_price,
        }
        for p in violations
    ]
    return Response({'count': len(results), 'results': results})
