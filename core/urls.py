from django.urls import path
from .views import UnsubscribeView, SendEmailView

urlpatterns = [
    path('unsub/<int:pk>/', UnsubscribeView.as_view()),
    path('sendmail/', SendEmailView.as_view()),
]