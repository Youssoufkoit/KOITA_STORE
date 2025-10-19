from cart.views import get_or_create_cart

def cart_count(request):
    cart = get_or_create_cart(request)
    cart_items_count = cart.items.count()
    return {
        'cart_items_count': cart_items_count,
        'cart_total_items': sum(item.quantity for item in cart.items.all())
    }