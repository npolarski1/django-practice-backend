"""
URL configuration for backend_practice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from conduit import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users', views.create_user),
    path('api/users/login', views.login),
    path('api/user', views.current_user),
    path('api/profiles/<str:username>', views.get_profile_by_username),
    path('api/profiles/<str:username>/follow', views.follow_unfollow_user_by_username),
    path('api/articles', views.get_create_articles),
    path('api/articles/feed', views.get_articles_feed),
    path('api/articles/<slug:slug>', views.get_update_delete_article),
    path('api/articles/<slug:slug>/comments', views.get_addto_article_comments),
    path('api/articles/<slug:slug>/comments/<int:id>', views.delete_article_comment),
    path('api/articles/<slug:slug>/favorite', views.create_delete_article_favorite),
    path('api/tags', views.get_tags)
]
