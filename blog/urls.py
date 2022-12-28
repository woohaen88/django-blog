from django.urls import path
from . import views

urlpatterns = [
    path("create_post/", views.PostCreate.as_view(), name="create_post"),
    path("tag/<str:slug>/", views.tag_page),
    path("category/<str:slug>/", views.category_page),
    path("<int:pk>/", views.PostDetail.as_view(), name="post_detail"),
    path("", views.PostList.as_view(), name="post_list"),
]
