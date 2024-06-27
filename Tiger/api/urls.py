from django.urls import path, include
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path("categoryData", categoryData, name="categoryData"),
    path("productData", productData, name="productData"),
    path("searchProduct", searchProduct, name="searchProduct"),
    path("categoryProduct", categoryProduct, name="categoryProduct"),
    path("subCategoryProduct", subCategoryProduct, name="subCategoryProduct"),
    path("categoryProductSort", categoryProductSort, name="categoryProduct"),
    path("subCategoryProductSort", subCategoryProductSort, name="subCategoryProduct"),
    path("filterProducts", filterProducts, name="filterProducts"),
    path("create-account/", CreateAccountView.as_view(), name='create-account'),
    path("business-registration/", BusinessRegistrationView.as_view(), name='business-registration'),
    path("bank-details/", BankDetailsView.as_view(), name='bank-details'),
    path("store-creation/", StoreCreationView.as_view(), name='store-creation'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)