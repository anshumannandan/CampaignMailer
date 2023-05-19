from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task(bind = True)
def send_campaign_email(self, host_url, campaign, user):

    user_id = user.get('id')

    context = {
        'user' : user.get('first_name'),
        'campaign' : campaign,
        'unsubscribe_url' : f'http://{host_url}/core/unsub/{user_id}/'
    }
    html_content = render_to_string('email.html', context)
    email = EmailMultiAlternatives(
        campaign.get('subject'),
        campaign.get('plain_text_content'),
        settings.EMAIL_HOST_USER,
        [user.get('email')]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()

    return 'EMAIL SENT'