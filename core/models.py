from django.db import models
from userauth.models import User
from taggit.managers import TaggableManager
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Avg

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (0, "☆☆☆☆☆"),
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

# path to the  to the images of the user or profile images
def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


############ category model #######################


class Category(models.Model):
    cid = ShortUUIDField(
        length=16,
        max_length=40,
        prefix="catid_",
        alphabet="abcdefg1234",
        primary_key=True,
    )
    title = models.CharField(max_length=100, default="food")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


############################## Vendor model ######################################
############################## Vendor model ######################################
############################## Vendor model ######################################


class Vendor(models.Model):
    vid = ShortUUIDField(
        length=16,
        max_length=40,
        prefix="venid_",
        alphabet="abcdefg1234",
        primary_key=True,
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100, default="nestify")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    description = RichTextUploadingField(
        null=True, blank=True, default="I am the nestify vendor, trustworthy"
    )
    contact = models.CharField(max_length=100, default="123, mainstreet london")
    address = models.CharField(max_length=100, default="+123 (456) 789")
    resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Tag(models.Model):
    pass


############################## Product model ######################################
############################## Product model ######################################
############################## Product model ######################################
class Product(models.Model):
    pid = ShortUUIDField(
        length=16,
        max_length=40,
        alphabet="abcdefg1234",
        unique=True,
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name="products"
    )

    title = models.CharField(max_length=100, default="Bananas")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = RichTextUploadingField(
        null=True, blank=True, default="This is the product description"
    )
    price = models.DecimalField(
        max_digits=999999999999, decimal_places=2, default="1.99"
    )
    old_price = models.DecimalField(
        max_digits=999999999999, decimal_places=2, default="2.99"
    )
    specifications = RichTextUploadingField(null=True, blank=True)
    stock_items = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    tags = TaggableManager(blank=True)

    # tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review"
    )

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(
        length=4, max_length=10, prefix="sku", alphabet="1234567890", unique=True
    )

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    def get_discount_percentage(self):
        discount = self.old_price - self.price
        percentage_discount = (discount / self.old_price) * 100
        return percentage_discount

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def average_rating(self):
        return (
            round(self.product_review.aggregate(Avg("rating"))["rating__avg"], 1) or 0
        )

    def percentage_avg_rating(self):
        avg_rating = self.average_rating()
        return round((avg_rating / 5) * 100, 1) if avg_rating else 0


class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images", default="product.jpg")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="productimages"
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"


############################## cart model ######################################
############################## cart model ######################################
############################## cart model ######################################

############### remember to create a cartitem model for users ################
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def total_price(self):
        total = sum(cart_item.get_total_price() for cart_item in self.cartitem_set.all())
        return total

    def item_count(self):
        return sum(cart_item.quantity for cart_item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


    def get_total_price(self):
        return self.item.price * self.quantity




class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartOrderItems')
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOICE, max_length=10, default="processing"
    )

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def total_price(self):
        total = sum(cart_item.get_total_price() for cart_item in self.cartorderitems_set.all())
        return total

    def item_count(self):
        return sum(cart_item.quantity for cart_item in self.cartorderitems_set.all())



    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    invoice_number = models.CharField(max_length=200)


    class Meta:
        verbose_name_plural = "Cart Order Items"

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


    def get_total_price(self):
        return self.item.price * self.quantity




# ############################## Product review, wishlist, address. ############


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_review"
    )
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating

    def get_rating_percentage(self):
        rating_percentage = (self.rating / 5) * 100
        return rating_percentage


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title


class AddressBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100,default='Ekpoma')
    state = models.CharField(max_length=100, default = 'Edo State')
    is_default = models.BooleanField(default=False)
    mobile = models.CharField(max_length=200, default='09030748341')

    class Meta:
        verbose_name_plural = "Address Book"

