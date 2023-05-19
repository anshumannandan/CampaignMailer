from rest_framework import views, generics, response, status, permissions
from . models import User, Campaign
from . serializers import SubscriberSerializer, CampaignSerializer
from . tasks import send_campaign_email
from celery import group


class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscriberSerializer


class AddCampaignView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CampaignSerializer


class UnsubscribeView(generics.UpdateAPIView):
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        request.method = 'PATCH'
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return response.Response({'message' : f'{instance.email} has been unsubscribed'})
    

class SendEmailView(views.APIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Campaign.objects.filter(active = True)
    
    def post(self, request, *args, **kwargs):

        campaign = request.GET.get('campaign')
        if campaign is None:
            campaign = self.queryset.first()
        else:
            try:
                campaign = self.queryset.get(id = campaign)
            except Campaign.DoesNotExist:
                return response.Response({'message' : 'Invalid Campaign ID'}, status=status.HTTP_404_NOT_FOUND)

        users = User.objects.filter(is_active=True)
        host_url = request.get_host()
        campaign = CampaignSerializer(campaign).data

        group(send_campaign_email.s(host_url, campaign, SubscriberSerializer(user).data) for user in users).apply_async()

        return response.Response({'message' : 'Campaign Emails sent to all active users'})