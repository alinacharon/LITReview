from django.urls import path
from . import views

urlpatterns = [
    path('manage_review/create/<int:ticket_id>/', views.manage_review, name='create_review'),
    path('manage_review/edit/<int:review_id>/', views.manage_review, name='edit_review'), 
    path('manage-ticket/', views.manage_ticket, name='create_ticket'),
    path('manage-ticket/<int:ticket_id>/', views.manage_ticket, name='edit_ticket'),
    path('create-review-without-ticket/', views.create_review_without_ticket, name='create_review_without_ticket'),
    path('', views.feed, name='feed'),
    path('posts/', views.user_posts, name='user_posts'),  
    path('delete-ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),   
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'), 
]

