from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search_posts, name='search'),
    path('about/', views.about, name='about'),
    path('accounts/register/', views.register_user, name='register'),
    # path('accounts/change_password/', views.change_password, name='change_password'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('bookmark_post/<slug:slug>', views.bookmark_post, name='bookmark_post'),
    path('like_post/<slug:slug>', views.like_post, name='like_post'),
    path('all_bookmark_posts/', views.all_bookmark_posts,
         name='all_bookmarked_posts'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('all_liked_posts/', views.all_liked_posts, name='all_liked_posts'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),
]
