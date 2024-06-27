from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin


class CategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["name", "description", "link", "display_category"]
    search_fields = ["name", "description", "link", "display_category"]
    list_editable = ["display_category"]


class SubCategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["name", "description", "category", "link"]
    search_fields = ["name", "description", "category", "link"]


class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["name","link","brand","category","subcategory","rating"]
    search_fields = ["name","link","brand","category__name","subcategory__name","rating"]


class MerchantAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["name", "link"]
    search_fields = ["name", "link"]


class ProductOfferAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["product","price","discount","cashback"]
    search_fields = ["product","price","discount","cashback"]


class StoreAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["name","link","cashback_type","storeName","rating_value","rating_count"]
    search_fields = ["name","link","cashback_type","storeName","rating_value","rating_count"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(ProductOffer, ProductOfferAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(CustomUser)
admin.site.register(BusinessRegistration)