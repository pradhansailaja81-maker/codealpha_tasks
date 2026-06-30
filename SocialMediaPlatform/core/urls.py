from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("signup/", views.signup, name="signup"),

    path("login/", views.user_login, name="login"),

    path("logout/", views.user_logout, name="logout"),
    path("create-post/", views.create_post, name="create_post"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("post/edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("post/delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("search/", views.search_users, name="search_users"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("unfollow/<str:username>/", views.unfollow_user, name="unfollow_user"),
]