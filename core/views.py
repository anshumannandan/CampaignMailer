from rest_framework import views, generics, response, status, permissions
from . models import User, Campaign
from . serializers import SubscriberSerializer, CampaignSerializer
from . utils import parallel_emails, CustomError


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
    querset = Campaign.objects.filter(active = True)
    
    def post(self, request, *args, **kwargs):

        campaign = request.GET.get('campaign')
        if campaign is None:
            campaign = self.querset.first()
        else:
            try:
                campaign = self.querset.get(id = campaign)
            except Campaign.DoesNotExist:
                raise CustomError(error='invalid campaign id', code=status.HTTP_404_NOT_FOUND)

        users = User.objects.filter(is_active=True)
        parallel_emails(request, campaign, users)
        return response.Response({'message' : 'Campaign Emails sent to all active users'})