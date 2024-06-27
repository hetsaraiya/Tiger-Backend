from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from .models import BusinessRegistration
from django.db import models
from django.contrib.auth import get_user_model
import jwt
from django.contrib.auth.hashers import make_password
from .models import *
import json
import requests
import os


@api_view()
def categoryData(request):
    categories = Category.objects.all()
    data = []
    for cat in categories:
        subCat = []
        subcats = SubCategory.objects.filter(category=cat).all()
        for sub in subcats:
            subCat.append({
                "name": sub.name,
                "link": sub.link
            })
        data.append({
            "name": cat.name,
            "link": cat.link,
            "subCategory": subCat,
            "isMain": cat.display_category
        })
    return Response(data)


@api_view()
def productData(request):
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 25)
    products = Product.objects.all()[int(page) * int(size) - int(size):int(page) * int(size)]
    data = []
    for product in products:
        data.append({
            "name": product.name,
            "link": product.link,
            "price": product.basePrice,
            "image": product.image_url,
            "merchant": product.merchant.name
        })
    return Response(data)


@api_view()
def searchProduct(request):
    query = request.GET.get("query", "")
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 25)
    products = Product.objects.filter(name__icontains=query)[int(page) * int(size) - int(size):int(page) * int(size)]
    data = []
    for product in products:
        data.append({
            "name": product.name,
            "link": product.link,
            "price": product.basePrice,
            "image": product.image_url,
            "merchant": product.merchant.name
        })
    return Response(data)


@api_view()
def categoryProduct(request):
    category = request.GET.get("category", "")
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 25)
    products = Product.objects.filter(category__link=category)[int(page) * int(size) - int(size):int(page) * int(size)]
    if len(products) == 0:
        return Response({"error": "No products found in this category"})
    data = []
    for product in products:
        offers = ProductOffer.objects.filter(product=product).all()
        data.append({
            "name": product.name,
            "link": product.link,
            "price": product.basePrice,
            "image": product.image_url,
            "offers": len(offers)
        })
    return Response(data)


@api_view()
def subCategoryProduct(request):
    subcategory = request.GET.get("subcategory", "")
    page = request.GET.get("page", 1)
    size = request.GET.get("size", 25)
    products = Product.objects.filter(subcategory__link=subcategory)[int(page) * int(size) - int(size):int(page) * int(size)]
    if len(products) == 0:
        return Response({"error": "No products found in this category"})
    data = []
    for product in products:
        data.append({
            "name": product.name,
            "link": product.link,
            "price": product.basePrice,
            "image": product.image_url,
            "merchant": product.merchant.name
        })
    return Response(data)

@api_view()
def categoryProductSort(request):
    category_link = request.GET.get("category", "")
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 25))
    order_by = request.GET.get("order_by", "asc")
    
    if order_by == "desc":
        sort_order = "-basePrice"
    else:
        sort_order = "basePrice"
    
    products = Product.objects.filter(category__link=category_link).order_by(sort_order)[(page - 1) * size: page * size]
    
    if not products:
        return Response({"error": "No products found in this category"})

    data = []
    for product in products:
        offers = ProductOffer.objects.filter(product=product)
        data.append({
            "name": product.name,
            "link": product.link,
            "price": product.basePrice,
            "image": product.image_url,
            "offers": len(offers)
        })
    return Response(data)

@api_view()
def subCategoryProductSort(request):
    subcategory_link = request.GET.get("subcategory", "")
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 25))
    order_by = request.GET.get("order_by", "asc")
    
    if order_by == "desc":
        sort_order = "-basePrice"
    else:
        sort_order = "basePrice"
    
    products = Product.objects.filter(subcategory__link=subcategory_link).order_by(sort_order)[(page - 1) * size: page * size]
    
    if not products:
        return Response({"error": "No products found in this category"})

    data = []
    for product in products:
        data.append({
            "name": product.name,
            "link": product.link,
            "price": product.basePrice,
            "image": product.image_url,
            "merchant": product.merchant.name
        })
    return Response(data)

@api_view()
def filterProducts(request):
    query = request.GET.get("query", "")
    category = request.GET.get("category", "")
    subcategory = request.GET.get("subcategory", "")
    rating = request.GET.get("rating", None)
    min_price = request.GET.get("min_price", None)
    max_price = request.GET.get("max_price", None)
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 25))
    product_query = Product.objects.all()
    if query:
        product_query = product_query.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        product_query = product_query.filter(category__name=category)
    if subcategory:
        product_query = product_query.filter(subcategory__name=subcategory)
    if min_price is not None:
        product_query = product_query.filter(basePrice__gte=min_price)
    if max_price is not None:
        product_query = product_query.filter(basePrice__lte=max_price)
    start = (page - 1) * size
    end = page * size
    products = product_query[start:end]
    data = []
    for product in products:
        data.append({
            "name": product.name,
            "link": product.link,
            "price": product.basePrice,
            "image": product.image_url,
            "merchant": product.merchant.name
        })
    
    return Response(data)

@api_view()
def topDeals(request):
    num_deals = int(request.GET.get("num_deals", 10))
    top_deals = Product.objects.all() \
        .annotate(max_discount=models.Max('offers__discount')) \
        .order_by('-max_discount')[:num_deals]
    data = []
    for deal in top_deals:
        offers = ProductOffer.objects.filter(product=deal).order_by('-discount')
        best_offer = offers[0] if offers.exists() else None

        data.append({
            "name": deal.name,
            "link": deal.link,
            "price": deal.basePrice,
            "image": deal.image_url,
            "merchant": deal.merchant.name,
            "best_offer": {
                "price": best_offer.price if best_offer else None,
                "discount": best_offer.discount if best_offer else None,
            }
        })

    return Response(data)

@api_view()
def todayDeals(request):
    num_deals = int(request.GET.get("num_deals", 10))
    current_date = timezone.now().date()
    today_deals = Product.objects.filter(offers__start_date__lte=current_date, offers__end_date__gte=current_date) \
        .distinct()[:num_deals]
    data = []
    for deal in today_deals:
        offers = ProductOffer.objects.filter(product=deal, start_date__lte=current_date, end_date__gte=current_date)
        best_offer = offers.order_by('-discount').first()

        data.append({
            "name": deal.name,
            "link": deal.link,
            "price": deal.basePrice,
            "image": deal.image_url,
            "merchant": deal.merchant.name,
            "best_offer": {
                "price": best_offer.price if best_offer else None,
                "discount": best_offer.discount if best_offer else None,
            }
        })

    return Response(data)

@api_view()
def topKitchenAppliances(request):
    num_deals = int(request.GET.get("num_deals", 10))
    kitchen_category = "Kitchen Appliances"
    kitchen_appliances = Product.objects.filter(
        Q(category__name=kitchen_category) | Q(subcategory__name=kitchen_category)
    )[:num_deals]
    data = []
    for appliance in kitchen_appliances:
        offers = ProductOffer.objects.filter(product=appliance)
        best_offer = offers.order_by('-discount').first()

        data.append({
            "name": appliance.name,
            "link": appliance.link,
            "price": appliance.basePrice,
            "image": appliance.image_url,
            "merchant": appliance.merchant.name,
            "best_offer": {
                "price": best_offer.price if best_offer else None,
                "discount": best_offer.discount if best_offer else None,
            }
        })

    return Response(data)

# @api_view()
# def register(self, request):
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#         name = data.get('name')
#         email = data.get('email')
#         mobile_no = data.get('mobile_no')
#         password = data.get('password')

#         if not all([name, email, mobile_no, password]):
#             return Response({'error': 'All fields are required'}, status=400)

#         if CustomUser.objects.filter(email=email).exists():
#             return Response({'error': 'Email is already in use'}, status=400)

#         user = CustomUser.objects.create(
#             name=name,
#             email=email,
#             mobile_no=mobile_no,
#             password=make_password(password)
#         )

#         # Store user data in session
#         request.session['user_id'] = user.id
#         request.session['name'] = user.name
#         request.session['email'] = user.email
#         request.session['mobile_no'] = user.mobile_no

#         token = self.generate_jwt_token(user)
#         return Response({'message': 'User created successfully', 'token': token}, status=201)

#     except Exception as e:
#         return Response({'error': str(e)}, status=500)

# def generate_jwt_token(self, user):
#         expiration_time = timezone.now() + timedelta(days=1)  # Token expires in 1 day
#         payload = {
#             'user_id': user.id,
#             'exp': expiration_time,
#             'iat': timezone.now(),
#         }
#         token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#         return token

User = get_user_model()

class CreateAccountView(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        email = data.get('email')
        mobile_no = data.get('mobile_no')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not all([name, email, mobile_no, password, confirm_password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        request.session['account_data'] = {
            'name': name,
            'email': email,
            'mobile_no': mobile_no,
            'password': password,
        }
        return Response({"message": "Account information stored in session."}, status=status.HTTP_200_OK)

class BusinessRegistrationView(APIView):
    def post(self, request):
        data = request.data.copy()
        file = request.FILES.get('signature_image')
        
        if file:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            data['signature_image'] = file_url
        else:
            data['signature_image'] = ''

        required_fields = [
            'gstin_choice', 'business_name', 'pan_number', 'business_type',
            'business_email', 'business_mobile_number', 'address_line_1',
            'address_line_2', 'state', 'city', 'pincode', 'signature_image'
        ]
        
        if all(field in data for field in required_fields):
            request.session['business_data'] = data
            return Response({"message": "Business registration information stored in session."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

class BankDetailsView(APIView):
    def post(self, request):
        data = request.data
        bank_account_number = data.get('bank_account_number')
        bank_ifsc_code = data.get('bank_ifsc_code')
        bank_account_holder_name = data.get('bank_account_holder_name')
        bank_account_type = data.get('bank_account_type')

        if not all([bank_account_number, bank_ifsc_code, bank_account_holder_name, bank_account_type]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        request.session['bank_data'] = {
            'bank_account_number': bank_account_number,
            'bank_ifsc_code': bank_ifsc_code,
            'bank_account_holder_name': bank_account_holder_name,
            'bank_account_type': bank_account_type,
        }
        return Response({"message": "Bank details stored in session."}, status=status.HTTP_200_OK)

class StoreCreationView(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['store_display_name', 'primary_category', 'store_disc']
        if all(field in data for field in required_fields):
            request.session['store_data'] = data
            # Process and save all collected data to the database
            account_data = request.session.get('account_data')
            business_data = request.session.get('business_data')
            bank_data = request.session.get('bank_data')
            store_data = request.session.get('store_data')

            if not (account_data and business_data and bank_data and store_data):
                return Response({"error": "Session data is missing."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user = User.objects.create_user(
                email=account_data['email'],
                name=account_data['name'],
                mobile_no=account_data['mobile_no'],
                password=account_data['password']
            )

            # Create the business registration entry
            BusinessRegistration.objects.create(
                user=user,
                gstin_choice=business_data['gstin_choice'],
                business_name=business_data['business_name'],
                pan_number=business_data['pan_number'],
                business_type=business_data['business_type'],
                business_email=business_data['business_email'],
                business_mobile_number=business_data['business_mobile_number'],
                address_line_1=business_data['address_line_1'],
                address_line_2=business_data['address_line_2'],
                state=business_data['state'],
                city=business_data['city'],
                pincode=business_data['pincode'],
                gstin=business_data.get('gstin', ''),
                signature_image=business_data['signature_image'],
                bank_account_number=bank_data['bank_account_number'],
                bank_ifsc_code=bank_data['bank_ifsc_code'],
                bank_account_holder_name=bank_data['bank_account_holder_name'],
                bank_account_type=bank_data['bank_account_type'],
                store_display_name=store_data['store_display_name'],
                primary_category=store_data['primary_category'],
                store_disc=store_data['store_disc']
            )

            return Response({"message": "Store creation information stored and data saved."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
