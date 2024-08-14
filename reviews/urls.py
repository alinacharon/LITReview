from django.urls import path
from . import views

urlpatterns = [

    path('', views.feed, name='feed'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('create-review/', views.create_review, name='create_review'),
    path('create-review/<int:ticket_id>/', views.create_review, name='create_review_with_ticket'),
]