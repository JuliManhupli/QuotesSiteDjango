from django.urls import path

from . import views

app_name = 'quotes'
urlpatterns = [
    path('', views.all_quotes, name='home'),
    path('author/<str:author>/', views.author, name='author'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('top-tags/', views.top_tags, name='top_tags'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quotes, name='add_quote'),
    path('edit_quote/<int:quote_id>/', views.edit_quote, name='edit_quote'),
    path('delete/<int:quote_id>/', views.delete_quote, name='delete_quote'),
]