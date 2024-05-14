from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from store.forms import RegistrationForm,LoginForm
from store.models import Product,Basket,BasketItem,Size,Order

# Create your views here.

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render(request,"signin.html",{"form":form})
    
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=request.POST.get("username")
            pwd=request.POST.get("password")
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                login(request,user_obj)
                return redirect("index")
        return render(request,"signin.html",{"form":form})
    
class IndexView(TemplateView):
    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        if "category" in request.GET:
            category=request.GET.get("category")
            qs=qs.filter(category_object__name=category)
        return render(request,"index.html",{"data":qs})
    
class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Product.objects.get(id=id)
        return render(request,"product_detail.html",{"data":qs})
    
class AddToCartView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        size_name=request.POST.get("size")
        product_obj=Product.objects.get(id=id)
        size_obj=Size.objects.get(name=size_name)
        basket_obj=request.user.cart
        BasketItem.objects.create(basket_object=basket_obj,size_object=size_obj,product_object=product_obj)
        return redirect('cart')
    
class CartListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitems.filter(is_order_placed=False)
        return render(request,'cart.html',{"data":qs})
    
class BasketItemDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        BasketItem.objects.get(id=id).delete()
        return redirect('cart')

class BasketItemUpdateQuantityView(View):
    def post(self,request,*args,**kwargs):
        value=request.POST.get("action")
        basketitem_obj=BasketItem.objects.get(id=kwargs.get("pk"))
        if value == "inc":
            basketitem_obj.quantity+=1
        elif value == "dec":
            basketitem_obj.quantity-=1
        basketitem_obj.save()
        return redirect('cart')
    
class CheckOutView(View):
    def get(self,request,*args,**kwargs):

        return render(request,"checkout.html")
    
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("delivery_address")
        payment_method=request.POST.get("payment_mode")
        user_object=request.user
        basket_item_objects=user_object.cart.get_cart_items

        order_object=Order.objects.create(
            user_object=user_object,
            delivery_address=address,
            phone=phone,
            email=email,
            payment_mode=payment_method

        )

        for bi in basket_item_objects:
            order_object.basket_item_objects.add(bi)
            bi.is_order_placed=True
            bi.save()

        print(email,phone,address,payment_method)
        return redirect('index')
    
class MyOrderView(View):
    def get(self,request,*args,**kwargs):
        qs=Order.objects.filter(user_object=request.user).exclude(status="cancelled")
        return render(request,"myorders.html",{"data":qs})


class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    