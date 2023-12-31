from rest_framework import generics, permissions
from .models import User, Card, Follow
from .serializers import UnfollowUserSerializer, FollowsThisUserSerializer, ThisUserFollowsListSerializer, ProfileSerializer, CardSerializer, FollowUserSerializer
from cards.permissions import IsCardSenderOrReadOnly, IsProfileOwnerOrReadOnly, IsThisUserUnfollowingOrReadOnly

# Create your views here.


class ProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    '''
    Methods: GET, PATCH, DELETE
    PATCH and DELETE methods only able to be performed by profile owner
    '''
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "username"
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(sent_by_user=self.request.user)


class AllCardViewSet(generics.ListCreateAPIView):
    '''
    Methods: GET, POST
    List of all cards and can create a new card
    '''

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]


class OneCardViewSet(generics.RetrieveUpdateDestroyAPIView):
    '''
    Methods: GET, PATCH, DELETE
    PATCH and DELETE methods only able to be performed by sender of card
    '''
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsCardSenderOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(sent_by_user=self.request.user)

class UserSentViewSet(generics.ListAPIView):
    queryset = Card.objects.all()
    '''
    Methods: GET
    List of cards sent by signed-in user
    '''

    def get_queryset(self):
        return self.request.user.cards_sent
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserReceivedViewSet(generics.ListAPIView):
    '''
    Methods: GET
    List of cards sent to signed-in user
    '''
    queryset = Card.objects.all()

    def get_queryset(self):
        return self.request.user.cards_received
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]


class FollowUserViewSet(generics.CreateAPIView):
    '''
    Methods: POST
    Only signed-in user able to request to follow another user
    '''
    queryset = Follow.objects.all()
    serializer_class = FollowUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(this_user=self.request.user)


class UnfollowUserViewSet(generics.DestroyAPIView):
    '''
    Methods: DELETE
    Only signed-in user able to request to unfollow another user
    '''
    queryset = Follow.objects.all()
    serializer_class = UnfollowUserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsThisUserUnfollowingOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(this_user=self.request.user)


class ThisUserFollowsListViewSet(generics.ListAPIView):
    '''
    Methods: GET
    List of users that the signed-in user follows
    '''
    queryset = Follow.objects.all()

    def get_queryset(self):
        return self.request.user.followees
    serializer_class = ThisUserFollowsListSerializer


class FollowsThisUserViewSet(generics.ListAPIView):
    '''
    Methods: GET
    List of users that follow the signed-in user
    '''
    queryset = Follow.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user_this_user_is_following_id=user)
    serializer_class = FollowsThisUserSerializer
