from cart.views import get_or_create_cart
from store.models import Notification

def cart_count(request):
    cart = get_or_create_cart(request)
    cart_items_count = cart.items.count()
    
    # Ajouter le compte des notifications non lues
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(
            user=request.user, 
            is_read=False
        ).count()
    
    return {
        'cart_items_count': cart_items_count,
        'cart_total_items': sum(item.quantity for item in cart.items.all()),
        'unread_notifications_count': unread_notifications_count,
    }