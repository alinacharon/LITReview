from itertools import chain
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Ticket
from authentication.models import UserFollows
from .forms import ReviewForm, TicketForm


@login_required
def feed(request):
    """
    Display a feed of posts from users followed by the current user, reviews on the user's tickets,
    and reviews on the user's tickets by other users not followed by the current user.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        Rendered follows_feed.html template with sorted posts from followed users, user's own posts,
        and reviews on user's tickets by other users.
    """
    following_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    tickets = Ticket.objects.filter(user__in=following_users)
    reviews = Review.objects.filter(user__in=following_users)
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)
    user_reviewed_tickets = Review.objects.filter(user=request.user).values_list('ticket', flat=True)
    reviews_on_user_tickets = Review.objects.filter(ticket__in=user_tickets).exclude(user=request.user)

    posts = sorted(
        chain(
            ({'type': 'ticket', 'object': ticket, 'user_has_reviewed': ticket.id in user_reviewed_tickets} for ticket in
             tickets),
            ({'type': 'review', 'object': review} for review in reviews),
            ({'type': 'ticket', 'object': ticket, 'user_has_reviewed': ticket.id in user_reviewed_tickets} for ticket in
             user_tickets),
            ({'type': 'review', 'object': review} for review in user_reviews),
            ({'type': 'review', 'object': review} for review in reviews_on_user_tickets)
        ),
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

    template = 'reviews/manage_ticket.html'
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

    template = 'reviews/manage_review.html'

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

    tickets = Ticket.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)

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
def delete_post(request, post_type, post_id):
    """
    Handles the deletion of a post (review or ticket).

    Args:
    - request: The HttpRequest object
    - post_type: A string 'review' or 'ticket' indicating the type of post to delete
    - post_id: The ID of the post to delete

    Returns:
    - HttpResponse: Redirects to 'user_posts' after deletion or displays the confirmation page
    """
    if post_type == 'review':
        post = get_object_or_404(Review, id=post_id, user=request.user)
    elif post_type == 'ticket':
        post = get_object_or_404(Ticket, id=post_id, user=request.user)
    else:
        return HttpResponseBadRequest("Type de post invalide")

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            post.delete()
        return redirect('user_posts')

    context = {
        'post_type': post_type,
        'post': post
    }
    return render(request, 'reviews/delete_post.html', context)
