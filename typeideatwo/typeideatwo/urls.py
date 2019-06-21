from django.conf.urls import url
from django.contrib import admin

from blog.views import (
    IndexView, CategoryView, TagView, PostDetailView, SearchView,AuthorView
)
from config.views import links


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$',
        CategoryView.as_view(),
        name='category_lists'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag_lists'),
    url(r'^post/(?P<post_id>\d+).html',
        PostDetailView.as_view(),
        name='post_details'),
    url(r'^links/$', links, name='links'),
    # url(r'^super_admin/', admin.site.urls, name='super_admin'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),

    url(r'^admin/', admin.site.urls, name='admins')

]
