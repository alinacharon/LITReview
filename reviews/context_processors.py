def previous_url(request):
    return {
        'previous_url': request.META.get('HTTP_REFERER', '/')
    }