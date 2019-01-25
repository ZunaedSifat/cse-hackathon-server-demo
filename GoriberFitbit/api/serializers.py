from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('score', 'distance', 'leaps', 'heart_rate', 'target_distance', 'target_leaps')


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ('distance', 'leap_count', 'start_time', 'end_time')


class HeartRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ('bmp', 'timestamp')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
