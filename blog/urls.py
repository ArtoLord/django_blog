from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
    path('accounts/login/', views.LoginView.as_view()),
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]
