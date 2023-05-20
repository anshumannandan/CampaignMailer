from rest_framework import views, generics, response, status, permissions
from . models import User
from . serializers import SubscriberSerializer, CampaignSerializer
from . utils import assign_task_to_celery, validate_and_return_campaign


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
    
    def post(self, request, *args, **kwargs):
        campaign = validate_and_return_campaign(request)  
        if campaign is None:
            return response.Response({'message' : 'Invalid Campaign ID'}, status=status.HTTP_404_NOT_FOUND)       
        assign_task_to_celery(campaign)
        return response.Response({'message' : 'Campaign Emails sent to all active users'})