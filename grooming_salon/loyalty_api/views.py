import uuid
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from grooming_salon.loyalty_api.models import Loyalty, Voucher
from grooming_salon.loyalty_api.serializers import LoyaltySerializer

# Create your views here.
#-----------------------------------------------------------------------------------------------------------------------
class LoyaltyViewSet(viewsets.ModelViewSet):
    serializer_class = LoyaltySerializer

    # Dohvati trenutni Loyalty program
    def get_queryset(self):
        return Loyalty.objects.filter(user=self.request.user)

    # Napravi Loyalty program za trenutnog korisnika
    def create(self, request, *args, **kwargs):
        if Loyalty.objects.filter(user=request.user).exists():
            return Response({'error': 'Već ste član programa lojalnosti.'}, status=status.HTTP_400_BAD_REQUEST)

        loyalty = Loyalty.objects.create(user=request.user)
        serializer = self.get_serializer(loyalty)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def claim_voucher(self, request, pk=None):
        loyalty = self.get_object()


        if loyalty.current_points >= 5:
            # Generator nasumičnih karaktera za vaučer
            random_suffix = str(uuid.uuid4())[:4].upper()

            voucher_code = f'GROOM-20-{loyalty.id}-{random_suffix}'

            try:
                # Kreiranjem vaučera, loyalty.current_points se smanjuje za 5 zbog logike u Modelu (current_points = total - vouchers * 5)
                Voucher.objects.create(user=request.user, code=voucher_code)

                return Response({
                    'status': 'Vaučer kreiran!',
                    'code': voucher_code,
                    'message': 'Pokažite ovaj kod u salonu za 20% popusta.'
                })
            except IntegrityError:
                return Response({'error': 'Greška pri generisanju koda. Pokušajte ponovo.'}, status=400)

        return Response({'error': f'Nemate dovoljno poena. Trenutno imate {loyalty.current_points}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='use-voucher/(?P<voucher_id>[0-9]+)')
    def use_voucher(self, request, voucher_id=None):
        try:
            # Vaučer koji pripada trenutnom korisniku je iskorišćen
            voucher = Voucher.objects.get(id=voucher_id, user=request.user, is_used=False)
            voucher.is_used = True
            voucher.save()
            return Response({'status': 'success', 'message': 'Vaučer je uspešno iskorišćen!'})
        except Voucher.DoesNotExist:
            return Response({'status': 'error', 'message': 'Vaučer nije pronađen ili je već iskorišćen.'}, status=404)

#-----------------------------------------------------------------------------------------------------------------------
