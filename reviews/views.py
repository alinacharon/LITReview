from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from authentication.models import UserFollows
from .forms import ReviewForm, TicketForm
from itertools import chain
from django.http import HttpResponseForbidden

@login_required
def feed(request):
    """
    Display a feed of posts from users followed by the current user and reviews on the user's tickets.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        Rendered follows_feed.html template with sorted posts from followed users and reviews on user's tickets.
    """
    following_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    tickets = Ticket.objects.filter(user__in=following_users)
    reviews = Review.objects.filter(user__in=following_users)
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    user_reviewed_tickets = Review.objects.filter(user=request.user).values_list('ticket', flat=True)

    posts = sorted(
        [{'type': 'ticket', 'object': ticket, 'user_has_reviewed': ticket.id in user_reviewed_tickets} for ticket in tickets] +
        [{'type': 'review', 'object': review} for review in reviews] +
        [{'type': 'ticket', 'object': ticket, 'user_has_reviewed': ticket.id in user_reviewed_tickets} for ticket in user_tickets] +
        [{'type': 'review', 'object': review} for review in user_reviews],
        key=lambda x: x['object'].created_at,
        reverse=True
    )

    return render(request, 'reviews/feed.html', {'posts': posts})

@login_required
def manage_ticket(request, ticket_id=None):
    """
    Handle the creation and editing of a ticket.
    
    Args:
        request: The HTTP request object.
        ticket_id: The ID of the ticket to edit (optional for creating a new ticket).
    
    Returns:
        Redirect to feed on successful creation or user_posts on successful edit,
        or render the appropriate template.
    """

    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.user != request.user:
            return HttpResponseForbidden("Vous ne pouvez pas modifier ce ticket.")
    else:
        ticket = None

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            if ticket is None:  
                new_ticket.user = request.user
            new_ticket.save()
            if ticket is None:
                return redirect('feed') 
            else:
                return redirect('user_posts') 
    else:
        form = TicketForm(instance=ticket)

    template = 'reviews/create_ticket.html' if ticket is None else 'reviews/edit_ticket.html'
    return render(request, template, {'form': form, 'ticket': ticket})


@login_required
def manage_review(request, ticket_id=None, review_id=None):
    """
    Handle the creation and editing of a review.
    
    Args:
        request: The HTTP request object.
        ticket_id: Optional. The ID of the ticket for which the review is being created.
        review_id: Optional. The ID of the review being edited (if applicable).
    
    Returns:
        Redirects to 'feed' on creation or 'user_posts' on edit, or renders the appropriate template.
    """
    if review_id:
        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            return HttpResponseForbidden("Vous ne pouvez pas modifier cette critique.")
        ticket = review.ticket 
    else:
        review = None
        if ticket_id:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            existing_review = Review.objects.filter(ticket=ticket, user=request.user).exists()
            if existing_review:
                return HttpResponseForbidden("Vous avez déjà laissé une critique pour ce ticket. ")
        else:
            ticket = None

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            if ticket:  
                new_review.ticket = ticket
            new_review.save()
            if review: 
                return redirect('user_posts')
            else: 
                return redirect('feed')
    else:
        review_form = ReviewForm(instance=review)

    template = 'reviews/create_review.html' if review is None else 'reviews/edit_review.html'

    return render(request, template, {'review_form': review_form, 'ticket': ticket, 'review': review})


@login_required
def create_review_without_ticket(request):
    """
    Handle the creation of a new review along with a new ticket.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        Redirect to feed on successful creation, or render create_review_without_ticket.html template.
    """
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

@login_required
def user_posts(request):
    """
    Display all posts (tickets and reviews) created by the current user.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        Rendered posts.html template with user's posts.
    """
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

    return render(request, 'reviews/posts.html', {'posts': posts})

@login_required
def delete_ticket(request, ticket_id):
    """
    Handle the deletion of an existing ticket.
    
    Args:
        request: The HTTP request object.
        ticket_id: The ID of the ticket to delete.
    
    Returns:
        Redirect to user_posts on successful deletion, or render delete_ticket.html template.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            ticket.delete()
            return redirect('user_posts')
        else:
            return redirect('user_posts')
    
    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


@login_required
def delete_review(request, review_id):
    """
    Handle the deletion of an existing review.
    
    Args:
        request: The HTTP request object.
        review_id: The ID of the review to delete.
    
    Returns:
        Redirect to user_posts on successful deletion, or render delete_review.html template.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            review.delete()
            return redirect('user_posts')
        else:
            return redirect('user_posts')

    return render(request, 'reviews/delete_review.html', {'review': review})


