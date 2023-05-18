from rest_framework import views, generics, response
from . models import User, Campaign
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import threading 


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
    

def send_campaign_email(request, campaign, user):

    context = {
        'user' : user.first_name,
        'campaign' : campaign,
        'unsubscribe_url' : f'http://{request.get_host()}/core/unsub/{user.id}/'
    }
    html_content = render_to_string('email.html', context)
    email = EmailMultiAlternatives(
        campaign.subject,
        campaign.plain_text_content,
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()


class SendEmailView(views.APIView):
    
    def post(self, request, *args, **kwargs):

        campaign = request.GET.get('campaign')
        if campaign is None:
            campaign = Campaign.objects.filter(active=True).first()

        threads = []
        for user in User.objects.filter(is_active=True):
            thread = threading.Thread(target=send_campaign_email, args=(request, campaign, user))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return response.Response({'message' : 'Campaign Emails sent to all active users'})