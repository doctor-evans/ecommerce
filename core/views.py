from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag
from django.db.models import Avg
from core.forms import AddnewAddressForm, ProductReviewForm
from django.http import JsonResponse
import datetime
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

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

# Create your views here.
def index(request):
    products = Product.objects.filter(product_status="published", featured=True)
    context = {"products": products}
    return render(request, "core/index.html", context)


# ######### Category #########


def categoryView(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "core/category_list.html", context)


def categoryProductView(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    context = {"products": products, "category": category}
    return render(request, "core/category_product_list.html", context)


################ Vendor ##############


def vendorView(request):
    vendors = Vendor.objects.all()
    context = {"vendors": vendors}
    return render(request, "core/vendors.html", context)


def vendorDetailView(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status="published", vendor=vendor)
    context = {"vendor": vendor, "products": products}
    return render(request, "core/vendor-details.html", context)


################ Shop ##############


def shopFilter(request):
    products = Product.objects.filter(product_status="published")
    context = {"products": products}
    return render(request, "core/shop_filter.html", context)


def filter_productView(request):
    try:
        categories = request.GET.getlist("category[]")
        vendors = request.GET.getlist("vendor[]")

        products = (
            Product.objects.filter(product_status="published")
            .order_by("-date")
            .distinct()
        )

        if categories:
            products = products.filter(category__cid__in=categories).distinct()

        if vendors:
            products = products.filter(vendor__vid__in=vendors).distinct()

        data = render_to_string("core/async/shop-filter.html", {"products": products})
        return JsonResponse({"data": data})

    except Exception as e:
        print("Error occurred:", e)  # Log the error
        return JsonResponse({"error": str(e)}, status=500)


def tagView(request, tag_slug=None):
    products = Product.objects.filter(product_status="published")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {"products": products, "tag": tag}
    return render(request, "core/tags.html", context)


def productView(request):
    products = Product.objects.filter(product_status="published")
    context = {"products": products}
    return render(request, "core/product_list.html", context)


def productDetailView(request, pid):
    product = Product.objects.get(pid=pid)
    # productimages is the related_name linking the ...
    # ... product images model class and the product class
    # therefore product_images below give all the productimages related to a product.
    product_images = product.productimages.all()
    related_products = Product.objects.filter(category=product.category).exclude(
        pid=pid
    )
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )
    review_form = ProductReviewForm()
    if reviews:
        avg_rating_percent = (average_rating["rating"] / 5) * 100
    else:
        avg_rating_percent = 0

    make_review = True
    if request.user.is_authenticated:
        user_product_review_count = ProductReview.objects.filter(
            user=request.user, product=product
        ).count()
        if user_product_review_count > 0:
            make_review = False

    context = {
        "product": product,
        "product_images": product_images,
        "related_products": related_products,
        "reviews": reviews,
        "average_rating": average_rating,
        "avg_rating_percent": avg_rating_percent,
        "review_form": review_form,
        "make_review": make_review,
    }
    return render(request, "core/product_detail.html", context)


def addReviewForm(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    date = datetime.datetime.now()
    review_date = date.strftime("%d %B, %Y")

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    rating = request.POST["rating"]
    star_rating = (int(rating) / 5) * 100

    context = {
        "user": user.username,
        "review": request.POST["review"],
        "star_rating": star_rating,
        "review_date": review_date,
    }

    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    return JsonResponse(
        {"bool": True, "context": context, "average_rating": average_rating}
    )


def searchView(request):
    query = request.GET["query"]
    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "core/search.html", context)


# ###### code to add to cart. below it is chatgpt edited own.

# def add_to_cartView(request):
#     cart_product = {}

#     cart_product[request.GET["pid"]] = {
#         "title": request.GET["title"],
#         "qty": request.GET["qty"],
#         "price": request.GET["price"],
#         "image": request.GET["image"],
#         "pid" : request.GET["pid"]
#     }

#     if "cart_data_obj" in request.session:
#         if request.GET["pid"] in request.session["cart_data_obj"]:
#             cart_data = request.session["cart_data_obj"]
#             cart_data[request.GET["pid"]]["qty"] = int(
#                 cart_product[request.GET["pid"]]["qty"]
#             )
#             cart_data.update(cart_data)
#             request.session["cart_data_obj"] = cart_data
#         else:
#             cart_data = request.session["cart_data_obj"]
#             cart_data.update(cart_product)
#             request.session["cart_data_obj"] = cart_data

#     else:
#         request.session["cart_data_obj"] = cart_product

#     return JsonResponse(
#         {
#             "data": request.session["cart_data_obj"],
#             "total_cart_items": len(request.session["cart_data_obj"]),
#         }
#     )

@login_required(login_url=("userauth:login"))
def add_to_cart_view(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    product_id = request.GET.get("pid")
    product = get_object_or_404(Product, pid=product_id)

    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item = product)

    if not created:
        # if item already in cart
        cart_item.quantity += 1
        cart_item.save()


    else:
        # if item is new and not in cart
        cart_item.quantity = 1
        cart_item.save()


    return JsonResponse({
        'total_cart_items' : cart.item_count()
    })



@login_required(login_url=("userauth:login"))
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    context = {
        'cart_items': cart_items,
        'total_price': cart.total_price(),
        'cart_count': cart.item_count()
    }
    return render(request, 'core/cart.html', context)




@login_required(login_url=("userauth:login"))
def delete_from_cartView(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    product_id = request.GET.get("productPid")
    product = get_object_or_404(Product, pid=product_id)
    cart = get_object_or_404(Cart, user = request.user)

    try:
        cart_item = CartItem.objects.get(cart = cart, item = product)
        cart_item.delete()
        
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)
    
    remaining_items = CartItem.objects.filter(cart=cart)

    cart_items = [
        {
            'item_title': item.item.title,
            'item_price' : item.item.price,
            'item_image' : item.item.image,
            'item_pid' : item.item.pid,
            'quantity': item.quantity,
            'get_total_price':item.get_total_price()
        }
        for item in remaining_items
    ]

    context = render_to_string("core/async/cart-list.html", {
        'message': 'Item removed successfully',
        'cart_items': cart_items,
        'total_price': cart.total_price(),
        'cart_count': cart.item_count()
    })

    return JsonResponse({"data": context})


@login_required(login_url=("userauth:login"))
def update_cartView(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    product_id = request.GET.get("productPid")
    quantity = request.GET.get("quantity")

    if int(quantity) < 1:
        return redirect("core:index")
    

    product = get_object_or_404(Product, pid=product_id)
    cart = get_object_or_404(Cart, user = request.user)

    try:
        cart_item = CartItem.objects.get(cart = cart, item = product)
        cart_item.quantity = quantity
        cart_item.save()

    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)
    
    remaining_items = CartItem.objects.filter(cart=cart)

    cart_items = [
        {
            'item_title': item.item.title,
            'item_price' : item.item.price,
            'item_image' : item.item.image,
            'item_pid' : item.item.pid,
            'quantity': item.quantity,
            'get_total_price':item.get_total_price()
        }
        for item in remaining_items
    ]

    context = render_to_string("core/async/cart-list.html", {
        'message': 'Item removed successfully',
        'cart_items': cart_items,
        'total_price': cart.total_price(),
        'cart_count': cart.item_count()
    })

    return JsonResponse({"data": context, "cart_count": cart.item_count()})



@login_required(login_url=("userauth:login"))
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    user = request.user
    address = AddressBook.objects.get(user=request.user, is_default=True)
    
    context = {
        'cart_items': cart_items,
        'total_price': cart.total_price(),
        'cart_count': cart.item_count(),
        'user':user,
        'address':address
    }
    return render(request, 'core/checkout.html', context)


@login_required(login_url=("userauth:login"))
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    context = {'items':items}
    return render(request, 'core/wishlist.html', context)


@login_required(login_url=("userauth:login"))
def add_to_wishlist(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    product_id = request.GET.get("productPid")
    product = get_object_or_404(Product, pid=product_id)
    
    Wishlist.objects.get_or_create(user = request.user, product = product)

    wishitems = Wishlist.objects.filter(user=request.user)

    

    return JsonResponse({
        'wishitems' : wishitems.count()
    })


@login_required(login_url=("userauth:login"))
def delete_from_wishlist(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    product_id = request.GET.get("productPid")
    product = get_object_or_404(Product, pid=product_id)
    
    Wishlist.objects.get(user = request.user, product = product).delete()

    wishitems = Wishlist.objects.filter(user=request.user)

    context = render_to_string("core/async/wish-list.html", {
        'items': wishitems,
               
        
    })

    return JsonResponse({"data": context, 'wishitems' : wishitems.count(),})

   

# def clear_session(request):
#     request.session.flush()
#     return redirect("core:index")


@login_required(login_url=("userauth:login"))
def clear_cart(request):
    cart = get_object_or_404(Cart, user = request.user)

    CartItem.objects.filter(cart=cart).delete()

    return redirect("core:index")



# function for creating a cartorder and cartorderitem model


def submit_order(user):
    # Get the user's cart
    cart = get_object_or_404(Cart, user=user)

    # Create a new CartOrder
    cart_order = CartOrder.objects.create(
        user=user,
        paid_status=False,  # Change this based on your payment processing logic
        order_date=timezone.now(),
        product_status="processing"  # Default status
    )

    # Iterate through cart items and create CartOrderItems
    for cart_item in cart.cartitem_set.all():
        CartOrderItems.objects.create(
            order=cart_order,
            item=cart_item.item,
            quantity=cart_item.quantity,
            invoice_number=f"INV-{cart_order.id}-{cart_item.id}"  # Generate invoice number as needed
        )

    # Optionally, you can clear the cart after submitting the order
    cart.item.clear()  # Clears all CartItems; ensure this is your intended behavior

    return cart_order

@login_required(login_url=("userauth:login"))
def order_view(request):
    if request.method == 'GET':
        order = submit_order(request.user)
        
        print('order_success', order.id)
        print('this is the total order price', order.total_price())

        return redirect("core:cart_view")


@login_required(login_url=("userauth:login"))
def user_dashboard(request):
    orders = CartOrder.objects.filter(user= request.user).order_by('-id')
    user = request.user
    addresses = AddressBook.objects.filter(user=request.user)
    context = {
        'orders':orders,
        'user': user,
        'addresses': addresses,
    }
    return render(request, 'core/dashboard.html', context)

def set_default_address(request):
    if request.method == 'GET':
        address_id = request.GET.get("address_id")
        AddressBook.objects.filter(user=request.user).update(is_default=False)
        address = AddressBook.objects.get(user=request.user, id=address_id)
        address.is_default= True
        address.save()

        addresses = AddressBook.objects.filter(user=request.user)

        context = render_to_string("core/async/default-address.html", {
        'addresses': addresses,
        })

        return JsonResponse({'data':context})
    return JsonResponse({'success':False}, status = 400)

@login_required(login_url=("userauth:login"))
def orderitem_view(request, id):
    order = CartOrder.objects.get(user= request.user, id=id)
    orderitems = CartOrderItems.objects.filter(order=order)
    context = {
        'orderitems':orderitems
    }
    return render(request, 'core/orderitem.html', context)

@login_required(login_url=("userauth:login"))
def add_new_address(request):
    if request.method == "POST":
        form = AddnewAddressForm(request.POST or None)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            form.cleaned_data["address"]
            form.cleaned_data["city"]
            form.cleaned_data["state"]
            form.cleaned_data["mobile"]
            address.save()
            return redirect("core:dashboard")
    else:
        form = AddnewAddressForm()
    context = {'form':form}
    return render(request, 'core/new_address.html', context)


@login_required(login_url=("userauth:login"))
def vendor_dashboard(request):
    return render(request, 'core/vendor-dashboard.html')

@login_required(login_url=("userauth:login"))
def vendor_guide(request):
    return render(request, 'core/vendor-guide.html')
