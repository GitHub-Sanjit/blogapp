from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count

from app.models import Post, Comments, Tag, Profile, WebsiteMeta
from app.forms import CommentForm, SubscribeForm

# Create your views here.


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = "Subscribe Successfully."
            subscribe_form = SubscribeForm()

    context = {'posts': posts, 'top_posts': top_posts, 'recent_posts': recent_posts, 'subscribe_form': subscribe_form,
               'subscribe_successful': subscribe_successful, 'featured_blog': featured_blog, 'website_info': website_info}
    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                comment = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    context = {"post": post, 'form': form, 'comments': comments}
    return render(request, 'app/post.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)

    top_posts = Post.objects.filter(
        tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(
        tags__in=[tag.id]).order_by('-last_updated')[0:2]
    tags = Tag.objects.all()
    context = {'tag': tag, 'top_posts': top_posts,
               'recent_posts': recent_posts, 'tags': tags}
    return render(request, 'app/tag.html', context)


def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)

    top_posts = Post.objects.filter(
        author=profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(
        author=profile.user).order_by('-last_updated')[0:2]

    top_authors = User.objects.annotate(
        number=Count('post')).order_by('number')

    context = {'profile': profile, 'top_posts': top_posts,
               'recent_posts': recent_posts, 'top_authors': top_authors}
    return render(request, 'app/author.html', context)


def search_posts(request):
    search_query = ""
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    print('Search : ', search_query)
    context = {'posts': posts, 'search_query': search_query}
    return render(request, 'app/search.html', context)


def about(request):
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {'website_info': website_info}
    return render(request, 'app/about.html', context)
