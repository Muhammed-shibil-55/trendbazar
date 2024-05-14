from django.urls import path

from store import views


urlpatterns=[
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("logout/",views.SignOutView.as_view(),name="signout"),
    path("product/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),
    path("products/<int:pk>/carts/add/",views.AddToCartView.as_view(),name="addtocart"),
    path("cart/",views.CartListView.as_view(),name="cart"),
    path("cart/items/<int:pk>/remove/",views.BasketItemDeleteView.as_view(),name="cart-remove"),
    path("cart/item/<int:pk>/quantity/change/",views.BasketItemUpdateQuantityView.as_view(),name="cart-quantity-change"),
    path("checkout/",views.CheckOutView.as_view(),name="checkout"),
    path("myorders/all/",views.MyOrderView.as_view(),name="myorders")
]