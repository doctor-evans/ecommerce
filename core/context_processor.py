from django.shortcuts import render

from core.models import (
    Product,
    ProductImages,
    ProductReview,
    CartOrder,
    CartOrderItems,
    Category,
    AddressBook,
    Wishlist,
    Vendor,
    Cart,
    CartItem
)


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user = request.user)
        wishitems = Wishlist.objects.filter(user=request.user)
        cart_item_count = cart.item_count()
    else:
        cart_item_count = 0
        wishitems = {}
    try:
        addressbook = AddressBook.objects.get(user=request.user)
    except:
        addressbook = "Enter and Verify Your Address"

    context = {"categories": categories, "vendors": vendors, "addressbook": addressbook, "cart_item_count": cart_item_count, "wishitems":wishitems}

    return context
