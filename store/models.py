from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from django.db.models.signals import post_save

class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
class Size(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
class Brand(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=400,null=True,blank=True)
    size_object=models.ManyToManyField(Size)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand_object=models.ForeignKey(Brand,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="product_images",null=True,blank=True,default="product_images/default.jpg")
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    
class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.owner.username
    
    @property
    def get_cart_items(self):
        return self.cartitems.filter(is_order_placed=False)

    @property
    def cart_total(self):
        cart_items=self.get_cart_items
        basket_total=0
        if cart_items:
            basket_total=sum([item.item_total for item in cart_items])
                
        return basket_total
    
class BasketItem(models.Model):
    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitems")
    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)
    size_object=models.ForeignKey(Size,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_order_placed=models.BooleanField(default=False)

    @property
    def item_total(self):
        return self.quantity*self.product_object.price
    

class Order(models.Model):
    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="myorders")
    basket_item_objects=models.ManyToManyField(BasketItem)
    delivery_address=models.CharField(max_length=400)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=200)
    options=(("online","online"),("cod","cod"))
    payment_mode=models.CharField(max_length=200,choices=options,default="cod")
    order_id=models.CharField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)
    status_options=(("order_confirmed","Order Confirmed"),("dispatched","Dispatched"),("in_transit","In Transit"),("delivered","Delivered"),("cancelled","Cancelled"))
    status=models.CharField(max_length=200,choices=status_options,default="order_confirmed")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def order_total(self):
        basket_items=self.basket_item_objects.all()
        total=0
        for bi in basket_items:
            total+=bi.item_total

        return total



def basket_create(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)

post_save.connect(receiver=basket_create,sender=User)
