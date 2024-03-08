from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('compte/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name="logout"),

]

