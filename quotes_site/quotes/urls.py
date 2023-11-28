from django.urls import path

from . import views

app_name = 'quotes'
urlpatterns = [
    path('', views.all_quotes, name='home'),
    path('author/<str:author>/', views.author, name='author'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('top-tags/', views.top_tags, name='top_tags'),
]