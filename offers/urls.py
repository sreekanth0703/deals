"""offers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from deals import views as deal_urls
from custom_deals import views as custom_deal_urls
admin.autodiscover()

urlpatterns = [
    path('', deal_urls.home),
    path('admin/', admin.site.urls),

    #####   Deals Urls  ########
    # Login and Logout
    path('login/', deal_urls.login),
    path('member_login/', deal_urls.member_login),
    path('logout/', deal_urls.logout),

    # Dashboard
    path('home/', deal_urls.home),

    #Posts Page
    path('posts/', deal_urls.posts),
    path('insert_post/', deal_urls.insert_post),

    ##### Custom Deals Urls  ########
    path('display_posts/', custom_deal_urls.display_posts),
]
