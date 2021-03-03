from django.contrib.auth.models import User
from rest_framework.views import APIView


class ListUsers(APIView):
    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
