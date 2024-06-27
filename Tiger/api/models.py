from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
# api/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, mobile_no, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, mobile_no=mobile_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, mobile_no, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_no']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Use a unique related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Use a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class Category(models.Model):
    name = models.CharField(max_length=500, default="")
    description = models.TextField()
    link = models.CharField(max_length=500, default="")
    display_category = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=500, default="")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500, default="")
    link = models.CharField(max_length=500, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    product_description = models.JSONField(default=dict)
    varients = models.JSONField(default=dict)
    image_url = models.URLField(default="")
    image_urls = models.JSONField(default=dict)
    brochure_files = models.FileField(upload_to="brochures/", blank=True, null=True)
    cashback_url = models.URLField(default="")
    is_compared = models.BooleanField(default=False)
    brand = models.CharField(max_length=500)
    offer_type = models.CharField(max_length=500)
    basePrice = models.JSONField(default=dict)
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    rating_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    redirect_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Merchant(models.Model):
    name = models.CharField(max_length=500)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name="merchants", null=True, blank=True)
    link = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=500)
    link = models.CharField(max_length=500, unique=True)
    logo = models.URLField(default="")
    bannar = models.URLField(default="")
    short_description = models.TextField()
    cashback_type = models.CharField(max_length=500)
    full_description = models.TextField()
    storeName = models.CharField(max_length=500)
    seo_description = models.TextField()
    rating_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.product.name} - {self.price}"

class BusinessRegistration(models.Model):
    GSTIN_CHOICES = [
        ('I Have GSTIN Number', 'I Have GSTIN Number'),
        ('I Want To Sell Products That Exempt GSTIN', 'I Want To Sell Products That Exempt GSTIN'),
        ('I Don\'t Have GSTIN Number OR I Have Applied For GSTIN', 'I Don\'t Have GSTIN Number OR I Have Applied For GSTIN'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gstin_choice = models.CharField(max_length=54, choices=GSTIN_CHOICES)
    business_name = models.CharField(max_length=255, default="")
    pan_number = models.CharField(max_length=10, default="")
    business_type = models.CharField(max_length=100, default="")
    business_email = models.EmailField(blank=True, null=True, default="")
    business_mobile_number = models.CharField(max_length=15, blank=True, null=True, default="")
    address_line_1 = models.CharField(max_length=255, default="")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, default="")
    state = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    pincode = models.CharField(max_length=6, default="")
    gstin = models.CharField(max_length=15, blank=True, null=True, default="")
    signature_image = models.ImageField(upload_to='signatures/', blank=True, null=True, default="")
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)
    bank_ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    bank_account_holder_name = models.CharField(max_length=20, default="")
    bank_account_type = models.CharField(max_length=20, default="")
    store_display_name = models.CharField(max_length=20, default="")
    primary_category = models.CharField(max_length=30, default="")
    store_disc = models.TextField(default="")
    
    def __str__(self):
        return self.business_name
