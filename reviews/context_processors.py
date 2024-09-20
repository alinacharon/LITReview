"""
This module contains context processors for the Reviews application.

Context processors are functions that add variables to the context of every request,
making these variables available in all templates.
"""


def previous_url(request):
    """
    Adds the previous URL to the request context.

    This function retrieves the referrer URL (the previous page) from the HTTP
    headers of the request. If no referrer URL is found, it returns the site root ('/').

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the previous URL under the key 'previous_url'.
    """
    return {
        'previous_url': request.META.get('HTTP_REFERER', '/')
    }
