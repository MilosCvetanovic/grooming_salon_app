from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from grooming_salon.notifications_api.models import Notification
from grooming_salon.notifications_api.serializers import NotificationSerializer

# Create your views here.
# ----------------------------------------------------------------------------------------------------------------------
# Koristim APIView jer pruža nizak nivo apstrakcije i veću kontrolu/fleksibilnost nad custom logikom jer ne koristim full CRUD
class NotificationListView(APIView):
    # GET /api/notifications/ - lista svih notifikacija za ulogovanog korisnika

    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        unread_count = notifications.filter(is_read=False).count() # broj nepročitanih notifikacija

        return Response({'unread_count': unread_count, 'notifications': serializer.data})

# ----------------------------------------------------------------------------------------------------------------------
class NotificationMarkReadView(APIView):
    # PATCH /api/notifications/<pk>/mark-read/ - označi jednu notifikaciju kao pročitanu

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notifikacija nije pronađena.'},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

# ----------------------------------------------------------------------------------------------------------------------
class NotificationMarkAllReadView(APIView):
    # PATCH /api/notifications/mark-all-read/ - označi sve notifikacije kao pročitane

    permission_classes = [IsAuthenticated]

    def patch(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

        return Response({'message': 'Sve notifikacije su označene kao pročitane.'})

# ----------------------------------------------------------------------------------------------------------------------
class NotificationDeleteView(APIView):
    # DELETE /api/notifications/<pk>/delete/ - obriši notifikaciju

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({'error': 'Notifikacija nije pronađena.'}, status=status.HTTP_404_NOT_FOUND)

        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------------------------------------------------------------------------------------------------------------------
