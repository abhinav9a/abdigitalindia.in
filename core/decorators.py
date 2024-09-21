from django.db import transaction
from django.http import HttpResponseRedirect


def transaction_required(view_func):
    """Decorator to ensure that a view runs within a database transaction."""
    def _wrapped_view(request, *args, **kwargs):
        with transaction.atomic():
            return view_func(request, *args, **kwargs)
    return _wrapped_view
