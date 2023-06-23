from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, permissions
from .models import User, Card
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, CardSerializer

# Create your views here.

class ProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class CardViewSet(generics.ListCreateAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class UserSentViewSet(generics.ListAPIView):
    queryset = Card.objects.all()
    def get_queryset(self):
        return self.request.user.sent_by_user
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserReceivedViewSet(generics.ListAPIView):
    queryset = Card.objects.all()
    def get_queryset(self):
        return self.request.user.sent_to_user
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

class FollowerPostViewSet(generics.ListAPIView):
    queryset = Card.objects.all()
    def get_queryset(self):
        return self.request.user.sent_by_user
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]