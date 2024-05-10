from django.contrib import admin
from .models import ClothCategory,Cloth
# Register your models here.

@admin.register(ClothCategory)
class ClothCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'is_visible', 'sort')
    list_editable = ('name','is_visible', 'sort')
    list_filter = ('is_visible',)
    search_fields = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category','genre','color','size','brand','material','price','is_visible', 'sort')
    list_editable = ('name','is_visible', 'sort')
    prepopulated_fields = {'slug': ('name',)}