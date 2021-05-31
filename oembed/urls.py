from django.urls import path

from oembed import views

urlpatterns = [
    path('', views.post_renderer)
]