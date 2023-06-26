from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from cards.models import Card, User, Follow


class CardSerializer(serializers.ModelSerializer):

    sent_by_user = serializers.ReadOnlyField(source='sent_by_user.username')
    sent_to_user = serializers.ReadOnlyField(source='sent_to_user.username')

    class Meta:
        model = Card
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    followers = serializers.HyperlinkedRelatedField(
        many=True, view_name='user_followers', read_only=True)

    class Meta:
        model = User
        exclude = ['password']


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'
