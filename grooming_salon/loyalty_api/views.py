from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from grooming_salon.loyalty_api.models import Loyalty
from grooming_salon.loyalty_api.serializers import LoyaltySerializer


# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
class LoyaltyViewSet(viewsets.ModelViewSet):
    serializer_class = LoyaltySerializer

    def get_queryset(self):
        return Loyalty.objects.filter(user=self.request.user)

    # Pri ulasku u Loyalty program, inicijalizujemo ga sa trenutnim brojem zakazanih termina
    def perform_create(self, serializer):
        initial_points = self.request.user.appointments.count()
        serializer.save(user=self.request.user, points=initial_points)

    @action(detail=True, methods=['post'])
    def claim_voucher(self, request, pk=None):
        loyalty = self.get_object()

        if loyalty.points >= 5:
            loyalty.points -= 5
            loyalty.save()
            return Response({
                'status': 'Vaučer kreiran!',
                'code': f'GROOM-20-{loyalty.id}',
                'message': 'Pokažite ovaj kod u salonu za 20% popusta.'
            })
        return Response({'error': 'Nemate dovoljno poena'}, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------------------------------------------------------------------------------------------
