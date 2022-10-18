from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib import admin
from graphene_django.views import GraphQLView

urlpatterns = [
    path("", RedirectView.as_view(url='/admin')),
    path("admin/", admin.site.urls),
    path("graphql", GraphQLView.as_view(graphiql=False))
]
