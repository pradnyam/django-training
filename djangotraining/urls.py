"""djangotraining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from blog import views
#
urlpatterns = [
    url('^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url('^admin/', admin.site.urls, name='admin'),
    # url('^login/$', views.LoginView.as_view(), name='login'),
    url('^register/$', views.Register.as_view(), name='register'),
    url('^blog/$', views.BlogListView.as_view(), name='blog_list'),
    url('^blog/add/$', views.BlogFormView.as_view(), name='add_blog'),
    url('^blog/(?P<id>[0-9]+)/$', views.BlogFormView.as_view(), name='edit_blog'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
