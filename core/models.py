from django.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    subject = models.CharField(max_length=255)
    preview_text = models.TextField()
    article_url = models.URLField()
    html_content = models.TextField()
    plain_text_content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    schedule_for = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.subject