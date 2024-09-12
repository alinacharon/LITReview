from django.db import models
from django.conf import settings


class Ticket(models.Model):
    """
    Represents a ticket in the review.

    A ticket is a request for a review, typically for a book or article.
    """

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='tickets/', null=True, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Represents a review.

    A review is associated with a ticket and contains the user's rating and comments.
    """

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reviews')
    headline = models.CharField(max_length=128) 
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline} - {self.rating}/5"

