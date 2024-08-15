from django.shortcuts import render, redirect,get_object_or_404
from .models import Ticket, Review
from django.contrib.auth.decorators import login_required
from itertools import chain
from .forms import TicketForm, ReviewForm


@login_required
def feed(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user).order_by('-created_at')
    reviews = Review.objects.filter(user=user).order_by('-created_at')

    posts = sorted(
        chain(
            [{'type': 'ticket', 'object': ticket} for ticket in tickets],
            [{'type': 'review', 'object': review} for review in reviews],
        ),
        key=lambda post: post['object'].created_at,
        reverse=True
    )

    return render(request, 'reviews/feed.html', {'posts': posts})


@login_required
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')

        ticket = Ticket.objects.create(
            user=request.user,
            title=title,
            description=description,
            image=image
        )
        return redirect('feed')

    return render(request, 'reviews/create_ticket.html')


@login_required
def create_review(request, ticket_id=None):
    ticket = get_object_or_404(Ticket, id=ticket_id) 
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review = Review.objects.create(
            user=request.user, ticket=ticket, rating=rating, comment=comment)
        return redirect('feed')
    return render(request, 'reviews/create_review.html', {'ticket': ticket})

@login_required
def create_review_without_ticket(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            # Создаем новый билет
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            
            # Создаем новый обзор
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_review_without_ticket.html', context)