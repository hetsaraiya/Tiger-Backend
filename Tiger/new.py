from django.contrib.auth.models import User
from api.models import ApiCategory, ApiMerchant, ApiProduct, ApiProductOffer, ApiStore, ApiSubcategory
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

# Delete all records from your models
ApiCategory.objects.all().delete()
ApiMerchant.objects.all().delete()
ApiProduct.objects.all().delete()
ApiProductOffer.objects.all().delete()
ApiStore.objects.all().delete()
ApiSubcategory.objects.all().delete()

# Delete all records from other models
User.objects.all().delete()
Group.objects.all().delete()
Permission.objects.all().delete()
LogEntry.objects.all().delete()
ContentType.objects.all().delete()
Session.objects.all().delete()
