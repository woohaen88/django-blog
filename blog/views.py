from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView


class PostList(ListView):
    model = Post
    template_name = "blog/post_list.html"
    ordering = "-pk"
    context_object_name = "post_list"

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"
