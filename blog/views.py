from django.shortcuts import render
from .models import Post, Category, Tag
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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context["categories"] = Category.objects.all()
        context["no_category_post_count"] = Post.objects.filter(category=None).count()
        return context


def category_page(request, slug):

    if slug == "no_category":
        category = "미분류"
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        "post_list": post_list,
        "categories": Category.objects.all(),
        "no_category_post_count": Post.objects.filter(category=None).count(),
        "category": category,
    }
    return render(request, "blog/post_list.html", context=context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        "post_list": post_list,
        "tag": tag,
        "categories": Category.objects.all(),
        "no_category_post_count": Post.objects.filter(category=None).count(),
    }

    return render(request, "blog/post_list.html", context=context)
