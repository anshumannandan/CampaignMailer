from rest_framework import generics, response
from . models import User, Campaign
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
    


def send_campaign_email(request):
    context = {
        'campaigns' : Campaign.objects.all(),
        'unsubscribe_url' : f'http://{request.get_host()}/core/unsub/{2}/'
    }
    html_content = render_to_string('email.html', context)
    plain_text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        'Subject',
        plain_text_content,
        settings.EMAIL_HOST_USER,
        ['anshumannandan2003@gmail.com']
    )

    email.attach_alternative(html_content, 'text/html')
    email.send()