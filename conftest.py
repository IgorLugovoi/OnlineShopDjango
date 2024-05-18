import os
import django
import OnlineShopDjango.settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineShopDjango.settings')
django.setup()
