from django.urls import path

from .views import *

urlpatterns = [
    # List all posts and create a new one
    path("posts", ListCreatePostView.as_view()),
    path("posts/<int:pk>", RetrievePostView.as_view()),  # Get post by ID
    path("posts/<int:pk>/update", UpdatePostView.as_view()),  # Update a post

    # List all polls and create a new one
    path("polls", ListCreatePollView.as_view()),
    path("polls/<int:pk>", RetrievePollView.as_view()),  # Get poll by ID
    
    path("polls/answer", UserPollAnswerCreateView.as_view())
]