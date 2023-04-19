from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.urls import reverse

from .models import Post

from django.views.generic import ListView

from django.views import View

from .forms import CommentForm

class StartingPage (ListView):
    
    template_name = "blog/index.html"

    model = Post

    ordering = ["-date"]

    context_object_name = "posts"

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set[:3]
        return data



class ALLPosts (ListView):
    template_name = "blog/all-posts.html"

    model = Post

    ordering = ["-date"]

    context_object_name = "all_posts"


class Post_Detail (View) :
    
    def is_stored (self, request,post_id) :
        stored_posts = request.session.get("request_posts")

        if stored_posts is not None :
            saved_for_later = post_id in stored_posts
        
        else :
            saved_for_later = False
        
        return saved_for_later

    def get (self,request, slug):
        
        post = Post.objects.get(slug = slug)
        

        ctx = {
            "post" : post,
            "tags" : post.tags.all(),
            "comment_form" : CommentForm(),
            "comments" : post.comments.order_by("-id"),
            "saved_for_later" : self.is_stored(request, post.id),
        }

        return render (request, "blog/post-detail.html", ctx)

    

    def post(self, request, slug):
        post = Post.objects.get(slug = slug)

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():

            comment=comment_form.save(commit= False)

            comment.post = post

            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        

        ctx = {
            "post" : post,
            "tags" : post.tags.all(),
            "comment_form" : CommentForm(),
            "comments" : post.comments.all().oreder_by("-id"),
            "saved_for_later" : self.is_stored(request, post.id),
        }
        return render (request, "blog/post-detail.html", ctx)
    

class ReadLater (View):

    def get (self, request) :
        stored_posts = request.session.get("stored_posts")

        ctx = {
        }
        if stored_posts is None or len(stored_posts) == 0 :
            ctx["posts"] = []
            ctx["has_posts"] = False
        
        else :
            posts = Post.objects.filter(id__in = stored_posts)
            ctx["posts"] = posts
            ctx["has_posts"] = True
        
        return render (request,"blog/stored-posts.html", ctx)



    def post (self, request) :
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None :
            stored_posts = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:

            stored_posts.append(post_id)

        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")