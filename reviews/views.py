from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from .forms import ReviewForm, TicketForm
from itertools import chain

@login_required
def feed(request):
    # Fetch all tickets and reviews
    tickets = Ticket.objects.all().order_by('-created_at')
    reviews = Review.objects.all().order_by('-created_at')

    # Combine and sort the posts
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
        review_form = ReviewForm(request.POST) 

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user  
            review.ticket = ticket  
            review.headline = review_form.cleaned_data['headline']
            review.save() 

            return redirect('feed')
    else:
        review_form = ReviewForm()  

    context = {
        'ticket': ticket,
        'review_form': review_form,  
    }
    
    return render(request, 'reviews/create_review.html', context)

@login_required
def create_review_without_ticket(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            
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