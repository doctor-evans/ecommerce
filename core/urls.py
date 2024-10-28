from django.urls import path, include
from core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.productView, name="product_view"),
    path("shop-filter/", views.shopFilter, name="shop_filter"),
    path("category/", views.categoryView, name="category_view"),
    path("category/<cid>/", views.categoryProductView, name="category_product"),
    path("vendor/", views.vendorView, name="vendor_view"),
    path("vendor/<vid>/", views.vendorDetailView, name="vendor_detail_view"),
    path("products/<pid>/", views.productDetailView, name="product_detail"),
    path("products/tag/<tag_slug>", views.tagView, name="tag_view"),
    path("add_review_ajax/<pid>", views.addReviewForm, name="add_product_review"),
    path("search/", views.searchView, name="search_view"),
    path("product-filter/", views.filter_productView, name="product-filter"),
    path("add-to-cart/", views.add_to_cart_view, name="add-to-cart"),
    path("product/wishlist/", views.wishlist_view, name="wishlist"),
    path("shop/cart/", views.cart_view, name="cart_view"),
    path("delete-from-cart/", views.delete_from_cartView, name="delete-from-cart"),
    path("shop/checkout/", views.checkout_view, name="checkout"),
    path("update-cart/", views.update_cartView, name="update_cart"),
    path("clear-cart/", views.clear_cart, name="clear-cart"),
    path("add-to-wishlist/", views.add_to_wishlist, name='add-to-wishlist'),
    path("delete-from-wishlist/", views.delete_from_wishlist, name='delete-from-wishlist'),
    path("place-order/", views.order_view, name='order'),
    path("shop/dashboard/", views.user_dashboard, name='dashboard'),
    path("shop/dashboard/<id>", views.orderitem_view, name='orderitem'),
    path("set-default-address/", views.set_default_address, name = 'set-default-address'),
    path("add-new-address/", views.add_new_address, name='new-address'),
    path("vendor-guide/", views.vendor_guide, name = 'vendor-guide'),
    path("vendor-dashboard/", views.vendor_dashboard, name = 'vendor-dashboard'),
]
