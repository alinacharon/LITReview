from django.urls import path
from . import views

urlpatterns = [
    path('create-review/<int:ticket_id>/', views.create_review, name='create_review'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('create-review-without-ticket/', views.create_review_without_ticket, name='create_review_without_ticket'),
    path('', views.feed, name='feed'),
    path('posts/', views.user_posts, name='user_posts'), 
    path('edit-ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),   
    path('edit-review/<int:review_id>/', views.edit_review, name='edit_review'),   
    path('delete-ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),   
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'), 
    path('follows_feed/', views.follows_feed, name='follows_feed'), 
]

