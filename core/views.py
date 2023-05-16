from rest_framework import generics, response
from . models import User


class UnsubscribeView(generics.UpdateAPIView):
    queryset = User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return response.Response({'message' : f'{instance.email} Unsubscribed'})
