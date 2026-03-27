from .models import Category

def cart_count(request):
    cart = request.session.get('cart', {})
    count = sum(item.get('qty', 0) for item in cart.values())
    categories = Category.objects.filter(active=True).order_by('order')
    return {'cart_count': count, 'categories': categories}
