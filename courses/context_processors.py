from courses.models import Category

# context_processors.py
def category(request):
    categories = Category.objects.all()
    return {'categories': categories}