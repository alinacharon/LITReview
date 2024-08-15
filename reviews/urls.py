from django.urls import path
from . import views

urlpatterns = [
    path('create-review/<int:ticket_id>/', views.create_review, name='create_review'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('create-review-without-ticket/', views.create_review_without_ticket, name='create_review_without_ticket'),
    path('', views.feed, name='feed'),
]