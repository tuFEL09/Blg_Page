#from datetime import date

from django.db.models import fields
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import conf
from django.urls.conf import path
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm

#def get_date(post):
 #   return post['date']   #helping func to extract date as key to use in sorted method


# Create your views here.
class StartPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
        #sorted_posts = sorted(all_posts, key=get_date)
        #latest_post = sorted_posts[-3:]      #for varaible and below is for database
    

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

class PostDetailsView(View):

    def is_saved_post(self, request, post_id):
        stored_post = request.session.get("stored_post")

        if stored_post is not None:
            is_saved_for_later = post_id in stored_post
        else:
            is_saved_for_later = False

        return is_saved_for_later

    

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
         
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_saved_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)


    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(
                reverse("post-detail-page", args=[slug]))     

        
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_saved_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):    

    def get(self, request):
        stored_post = request.session.get("stored_post")

        context = {}

        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["posts"] = []
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_post = request.session.get("stored_post")

        if stored_post is None:
            stored_post = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
            
        request.session["stored_post"] = stored_post

        return HttpResponseRedirect("/")
        