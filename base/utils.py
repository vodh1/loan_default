from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

def auth_required(view_func):
    """
    Decorator for function-based views that requires authentication
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

def api_auth_required(view_func):
    """
    Decorator for API views that requires authentication
    """
    @wraps(view_func)
    @api_view(['GET', 'POST', 'PUT', 'DELETE'])
    @permission_classes([IsAuthenticated])
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper 