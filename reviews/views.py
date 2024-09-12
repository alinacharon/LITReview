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
    Display a feed of all tickets and reviews, sorted by creation date.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        Rendered feed.html template with sorted posts.
    """
    tickets = Ticket.objects.all().order_by('-created_at')
    reviews = Review.objects.all().order_by('-created_at')

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
    """
    Handle the creation of a new ticket.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        Redirect to feed on successful creation, or render create_ticket.html template.
    """
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
    """
    Handle the creation of a new review for a specific ticket.
    
    Args:
        request: The HTTP request object.
        ticket_id: The ID of the ticket to review (optional).
    
    Returns:
        Redirect to feed on successful creation, or render create_review.html template.
    """
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
def edit_ticket(request, ticket_id):
    """
    Handle the editing of an existing ticket.
    
    Args:
        request: The HTTP request object.
        ticket_id: The ID of the ticket to edit.
    
    Returns:
        Redirect to user_posts on successful edit, or render edit_ticket.html template.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden("Vous ne pouvez pas modifier ce ticket.")

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def edit_review(request, review_id):
    """
    Handle the editing of an existing review.
    
    Args:
        request: The HTTP request object.
        review_id: The ID of the review to edit.
    
    Returns:
        Redirect to user_posts on successful edit, or render edit_review.html template.
    """
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("Vous ne pouvez pas modifier cette critique.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('user_posts')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})


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
    ticket = get_object_or_404(Ticket, id=ticket_id)

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
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            review.delete()
            return redirect('user_posts')
        else:
            return redirect('user_posts')

    return render(request, 'reviews/delete_review.html', {'review': review})

@login_required
def follows_feed(request):
    """
    Display a feed of posts from users followed by the current user and reviews on the user's tickets.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        Rendered follows_feed.html template with sorted posts from followed users and reviews on user's tickets.
    """
    following_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    tickets = Ticket.objects.filter(user__in=following_users)
    reviews = Review.objects.filter(user__in=following_users).exclude(user=request.user).order_by('-created_at')
    user_tickets = Ticket.objects.filter(user=request.user)
    reviews_on_user_tickets = Review.objects.filter(ticket__in=user_tickets).exclude(user=request.user)

    posts = sorted(
        [{'type': 'ticket', 'object': ticket} for ticket in tickets] +
        [{'type': 'review', 'object': review} for review in reviews] +
        [{'type': 'review', 'object': review} for review in reviews_on_user_tickets],
        key=lambda x: x['object'].created_at,
        reverse=True
    )

    return render(request, 'reviews/follows_feed.html', {'posts': posts})

