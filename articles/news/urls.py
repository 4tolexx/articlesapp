from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = "news"

urlpatterns = [
    path("create-post/", views.PostCreateView.as_view(), name="create-post"),
    path("create-comment/<int:pk>/", views.CommentCreateView.as_view(), name="create-comment"),
    path("article-detail/<int:pk>/", views.PostDetailView.as_view(), name="article-detail"),
    path("article-edit/<int:pk>/", views.PostEditView.as_view(), name="article-edit"),
    path("article-list/", views.PostListView.as_view(), name="article-list"),

    url(r"^(?P<username>[-\w]+)$", views.ProfileDetailView.as_view(), name="profile-detail"),
    url(r"^edit/$", views.ProfileEditView.as_view(), name="profile-edit"),
    
]

