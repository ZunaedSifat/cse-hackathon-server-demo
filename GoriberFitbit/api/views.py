from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from GoriberFitbit.api.serializers import UserSerializer, GroupSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        content = {
            'message': 'New project!'
        }
        return Response(content)


# Testing database models

class UserViewSet(viewsets.ModelViewSet):

    # Defines a 'queryset'
    queryset = User.objects.all().order_by('-date_joined')
    # Defines a 'serializer_class'
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
