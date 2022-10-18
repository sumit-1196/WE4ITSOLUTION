from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.contrib import admin
from graphene_django.views import GraphQLView
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("", RedirectView.as_view(url='/admin')),
    path("admin/", admin.site.urls),
    path("graphql", GraphQLView.as_view(graphiql=False)),
    re_path(r'^media/(?P<path>.*)$', serve,
        {'document_root':       settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]
