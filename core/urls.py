from django.urls import path
from .views import SubscribeView, UnsubscribeView, SendEmailView


urlpatterns = [
    path('sub/', SubscribeView.as_view()),
    path('unsub/<int:pk>/', UnsubscribeView.as_view()),
    path('sendmail/', SendEmailView.as_view()),
]