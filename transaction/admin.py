from django.contrib import admin
from .models import Transaction, TypeTransaction

# Register your models here.
admin.site.register(Transaction)
admin.site.register(TypeTransaction)
