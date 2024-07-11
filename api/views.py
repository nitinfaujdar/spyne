from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models import Q
 
from .models import *
from .serializers import *
from django.db.models import Q

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        user = User.objects.get(email=(request.data.get('email')))
        if not user.check_password(request.data.get('password')):
            raise serializers.ValidationError({"Error": "Invalid authentication credentials"})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Login Successfull", "data": token.key})


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return User.objects.filter(Q(username__icontains=query))
        return super().get_queryset()

class DiscussionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer

class DiscussionListView(generics.ListCreateAPIView):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer

    def get_queryset(self):
        tag = self.request.query_params.get('tag', None)
        text = self.request.query_params.get('text', None)
        if tag:
            return Discussion.objects.filter(hashtags__name__icontains=tag)
        if text:
            return Discussion.objects.filter(text__icontains=text)
        return super().get_queryset()

class CommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class FollowView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

