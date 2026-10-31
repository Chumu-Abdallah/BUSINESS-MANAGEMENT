from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ongeza/', views.ongeza_bidhaa, name='ongeza'),
    path('uza/<int:id>/', views.uza, name='uza'),
    path('futa/<int:id>/', views.futa, name='futa'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('users/', views.user_list, name='user_list'), #kwa boss kuona wauzaji
    path('futa-user/<int:id>/', views.futa_user, name="futa_user"),
    path('uza/<int:id>/<int:kiasi>/', views.uza, name='uza_zaidi'),
    path('ripoti/<int:mwaka>/', views.ripoti_mwaka, name='ripoti_mwaka'),
    path('ripoti/<int:mwaka_jana>/', views.ripoti_mwaka, name='ripoti_mwaka1'),
    path('toa_matumizi/', views.toa_matumizi, name='toa_matumizi'),
]