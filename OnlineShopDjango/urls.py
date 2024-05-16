from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main.views import home
from main.views import order_view
from itemList.views import ItemListHome
from main.views import show_category_items
from shopItem.views import shop_item_detail
from shopItem.views import add_to_cart
from shopItem.views import clear_cart
from shopItem.views import cartItem


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # path('shop/', shopItemHome, name='shopItemHome'),
    path('order/', order_view, name='order'),
    path('itemListHome/', ItemListHome, name='itemListHome'),
    path('category/<int:category_id>/', show_category_items, name='category_items'),
    # path('shopItem/', shopItemHome, name='shopItemHome'),
    path('shopItem/<slug:cloth_slug>/', shop_item_detail, name='shop_item_detail'),
    path('add-to-cart/<int:cloth_id>/', add_to_cart, name='add_to_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('cart/', cartItem, name='cart_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
