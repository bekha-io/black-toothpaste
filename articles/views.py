from django.shortcuts import render
from rest_framework import views
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.exceptions import APIException
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics

from .serializers import *


class BasicAuthenticationMixin:
    authentication_classes = [BasicAuthentication]


class UserPostIsAuthorQuerysetMixin(generics.GenericAPIView):
    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user)


class UserPollIsAuthorQuerysetMixin(generics.GenericAPIView):
    def get_queryset(self):
        return Poll.objects.filter(post__created_by=self.request.user)


# [POST, GET]
class ListCreatePostView(generics.ListCreateAPIView, BasicAuthenticationMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# [GET <PK>]
class RetrievePostView(generics.RetrieveAPIView, BasicAuthenticationMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# [PUT]
class UpdatePostView(generics.UpdateAPIView, BasicAuthenticationMixin, UserPostIsAuthorQuerysetMixin):
    serializer_class = PostSerializer


# [GET, POST]
class ListCreatePollView(generics.ListCreateAPIView, BasicAuthenticationMixin):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    
    def create(self, request, *args, **kwargs):
        # Checking whether user is the author of the given post before creating poll
        poll_serializer = PollSerializer(data=request.data)
        poll_serializer.is_valid(raise_exception=True)
        post = Post.objects.get(id=poll_serializer.data['post'])
        
        if post.created_by != self.request.user:
            raise APIException('You are not the author of this post', code=HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)



class RetrievePollView(generics.RetrieveAPIView, BasicAuthenticationMixin):
    model = Poll
    serializer_class = PollSerializer


class UpdatePollView(generics.UpdateAPIView, BasicAuthenticationMixin, UserPollIsAuthorQuerysetMixin):
    model = Poll
    serializer_class = PollSerializer


class UserPollAnswerCreateView(generics.CreateAPIView, BasicAuthenticationMixin):
    model = UserPollAnswer
    serializer_class = UserPollAnswerSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Checking whether user is the author of the given post before creating poll
        poll_answer_serializer = UserPollAnswerSerializer(data=request.data)
        poll_answer_serializer.is_valid(raise_exception=True)
        post = Poll.objects.get(id=poll_answer_serializer.data['poll'])
        
        if poll_answer_serializer.data['answer'] not in [i.id for i in post.options.all()]:
            raise APIException('This option does not belong to this poll', HTTP_422_UNPROCESSABLE_ENTITY)
        
        return super().create(request, *args, **kwargs)