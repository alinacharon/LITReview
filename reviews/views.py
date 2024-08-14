# reviews/views.py
from django.shortcuts import render, redirect
from .models import Ticket, Review
from django.contrib.auth.decorators import login_required

@login_required
def feed(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user).order_by('-created_at')
    reviews = Review.objects.filter(user=user).order_by('-created_at')

    from itertools import chain
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.created_at,
        reverse=True
    )

    return render(request, 'reviews/feed.html', {'posts': posts})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ticket = Ticket.objects.create(user=request.user, title=title, description=description)
        return redirect('feed')
    return render(request, 'reviews/create_ticket.html')

@login_required
def create_review(request, ticket_id=None):
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        ticket = None
        if ticket_id:
            ticket = Ticket.objects.get(id=ticket_id)
        review = Review.objects.create(user=request.user, ticket=ticket, rating=rating, comment=comment)
        return redirect('feed')
    return render(request, 'reviews/create_review.html', {'ticket_id': ticket_id})