from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trans/', include('transaction.urls')),
    path('api/users/', include('users.urls')),
    path('api/saving_money/', include('saving_money.urls')),
]
