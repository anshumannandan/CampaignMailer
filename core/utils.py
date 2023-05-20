from . models import User, Campaign
from . serializers import SubscriberSerializer, CampaignSerializer
from . tasks import send_campaign_email
from celery import group
from django.conf import settings


def assign_task_to_celery(campaign, eta=None):
    users = User.objects.filter(is_active=True)
    host_url = settings.DEFAULT_DOMAIN
    campaign = CampaignSerializer(campaign).data
    group(send_campaign_email.s(host_url, campaign, SubscriberSerializer(user).data) for user in users).apply_async(eta = eta)


def validate_and_return_campaign(request):
    queryset = Campaign.objects.filter(active=True)
    campaign_id = request.GET.get('campaign')
    if campaign_id:
        try:
            campaign = queryset.get(id=campaign_id)
        except Campaign.DoesNotExist:
            pass
    else:
        campaign = queryset.first()
    return campaign