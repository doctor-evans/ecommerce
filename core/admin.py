from django.contrib import admin
from django.db.models import Avg
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


# Register your models here.
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


class ProductImageAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = [
        "user",
        "title",
        "product_image",
        "price",
        "category",
        "vendor",
        "featured",
        "product_status",
        "average_rating",
        "percentage_avg_rating",
    ]

    def average_rating(self, obj):
        return round(obj.product_review.aggregate(Avg("rating"))["rating__avg"], 1) or 0

    def percentage_avg_rating(self, obj):
        avg_rating = self.average_rating(obj)
        return round((avg_rating / 5) * 100, 1) if avg_rating else 0

    percentage_avg_rating.short_description = "Percentage Rating"
    average_rating.short_description = "Average Rating"  # Customize the column header



class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product_count", "total_price"]
    
    def product_count(self, obj):
        return sum(cart_item.quantity for cart_item in obj.cartitem_set.all())
    product_count.short_description = _("Product Count")

    def total_price(self, obj):
        total = sum(cart_item.item.price * cart_item.quantity for cart_item in obj.cartitem_set.all())
        return total  # Format as currency
    total_price.short_description = _("Total Price")


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'item', 'quantity']
    



class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category_image"]


class VendorAdmin(admin.ModelAdmin):
    list_display = ["title", "vendor_image"]


class CartOrderAdmin(admin.ModelAdmin):
    list_display = ["user", "paid_status", "order_date", "product_status", "item_count", "total_price"]
    def item_count(self, obj):
        return sum(cart_item.quantity for cart_item in obj.cartorderitems_set.all())
    item_count.short_description = _("Item Count")

    def total_price(self, obj):
        total = sum(cart_item.item.price * cart_item.quantity for cart_item in obj.cartorderitems_set.all())
        return total  # Format as currency
    total_price.short_description = _("Total Price")


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "invoice_number",
        "item",
        "quantity",
    ]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "review", "rating"]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "date"]


class AddressBookAdmin(admin.ModelAdmin):
    list_display = ["user", "address", "is_default", "city", "state", "mobile"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(AddressBook, AddressBookAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
