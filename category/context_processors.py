# In Django, context processors are simple Python functions that provide additional context (data) to all your templates. This allows you to make certain variables or data available across multiple templates without having to pass them individually from each view.

from .models import Category


def categories_processor(request):
    categories = Category.objects.all()
    return {"categories": categories} # dictionary
