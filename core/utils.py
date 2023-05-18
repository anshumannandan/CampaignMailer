from rest_framework import status, exceptions
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import threading 


class CustomError(exceptions.APIException):

    def __init__(self, error, code = status.HTTP_400_BAD_REQUEST):
        self.status_code = code
        self.detail = {'message' : error}


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


def parallel_emails(request, campaign, users):

    threads = []
    for user in users:
        thread = threading.Thread(target=send_campaign_email, args=(request, campaign, user))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()