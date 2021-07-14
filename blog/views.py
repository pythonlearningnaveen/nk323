from django.db import connection
from django.shortcuts import render, get_object_or_404

# from datetime import date

from .models import Post, Author, Tag

from django.views.generic import ListView, DetailView
from .forms import Comment, CommentForm

from django.views import View

from django.http import HttpResponseRedirect
from django.urls import reverse

# all_posts = [
    
# ]

# all_posts = [
#     {
#         "slug" : "hike-in-the-mountains",
#         "image" : "mountains.jpg",
#         "author" : "Naveen",
#         "date" : date(2021, 6, 13),
#         "title" : "Mountain Hiking",
#         "excert" : """
#             There's nothing like the view you get when hiking in the mountain! 
#             And I wasen't even prepared for that what happend whilst 
#             I was enjoying the view!
#         """,
#         "content" : """
#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.

#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.

#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.
#         """
#     },

#     {
#         "slug" : "woods-in-jungle",
#         "image" : "woods.jpg",
#         "author" : "Naveen",
#         "date" : date(2021, 7, 14),
#         "title" : "Woods in Junle",
#         "excert" : """
#             Are you a nature lover? If you are the click to expore more.
#         """,
#         "content" : """
#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.

#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.

#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.
#         """
#     },

#     {
#         "slug" : "programming-is-fun",
#         "image" : "coding.jpg",
#         "author" : "Naveen",
#         "date" : date(2021, 7, 15),
#         "title" : "Programming is Fun",
#         "excert" : """
#             Did you spend hours searching that one error in your code? You need to join me.
#         """,
#         "content" : """
#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.

#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.

#             Lorem ipsum, dolor sit amet consectetur adipisicing elit. Nisi, 
#             ipsam! Molestias ducimus voluptatum pariatur id expedita dicta. O
#             fficia itaque vitae aliquid corrupti modi consequuntur odio, fuga nihil necessitatibus,
#             et velit.
#         """
#     }
# ]

# def get_date(post):
#     return post['date']

# Create your views here.

# def starting_page(request):

#     latest_post = Post.objects.all().order_by("-date")[:3] # soritng in descending order, Latest 3 post only

#     # sorted_post = sorted(all_posts, key=get_date)
#     # latest_post = sorted_post[-3:]
#     return render(request, "blog/index.html", {
#         "posts" : latest_post
#     })

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self) :
        queryset= super().get_queryset()
        data = queryset[:3]
        return data


def posts(request):
    all_posts = Post.objects.all().order_by("-date")

    return render (request, "blog/all-post.html",{
        "all_posts" : all_posts
    })

# class AllPostView (ListView):
#     template_name = "blog/all-post.html"
#     model = "Post"
#     ordering = ["-date"]
#     context_object_name = "all_posts"

# def post_detail(request, slug):
#     # identified_post = Post.objects.get(slug = slug)
#     identified_post = get_object_or_404(Post, slug=slug)

#     # identified_post= next(post for post in all_posts if post['slug']==slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })

# class SinglePostView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post
#     context_object_name = "post"

#     def get_context_data(self, **kwargs):
#         context= super().get_context_data(**kwargs)
#         context["post_tags"]= self.object.tags.all()
#         context['comment_form']= CommentForm
#         return context

class SinglePostView(View):

    def is_stored_posts(self, request, post_id):
        stored_posts= request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post= Post.objects.get(slug= slug)

        all_comment = post.comments.all().order_by("-id")
        if all_comment is None or len(all_comment)==0:
            has_comment=False
        else:
            has_comment=True

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": all_comment,
            "has_comment": has_comment,
            "saved_for_later": self.is_stored_posts(request, post.id)
        }
        
        return render (request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post= Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit= False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_posts(request, post.id)
        }
        return render (request, "blog/post-detail.html", context)


class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context={}

        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context["has_posts"]=False
        else:
            posts= Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_posts"]=True

        return render (request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        
        post_id=int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
            
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
