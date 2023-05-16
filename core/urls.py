from django.urls import path, include
from .views import UnsubscribeView

urlpatterns = [
    path('unsub/<int:pk>/', UnsubscribeView.as_view()),
]