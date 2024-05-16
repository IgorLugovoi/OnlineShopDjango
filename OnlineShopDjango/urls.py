from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main.views import home, view_cart_and_order,show_category_items
from itemList.views import ItemListHome
from shopItem.views import shop_item_detail,add_to_cart,clear_cart,cartItem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('shopItem/<slug:cloth_slug>/', shop_item_detail, name='shop_item_detail'),
    path('itemListHome/', ItemListHome, name='itemListHome'),
    # path('order/', order_view, name='order'),
    path('category/<int:category_id>/', show_category_items, name='category_items'),
    path('add-to-cart/<int:cloth_id>/', add_to_cart, name='add_to_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    # path('cart/', cartItem, name='cart_detail'),
    path('cart/', view_cart_and_order, name='cart_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
