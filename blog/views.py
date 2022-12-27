from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView


class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"
    ordering = "-pk"
    context_object_name = "post_list"


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/single_post_page.html"
