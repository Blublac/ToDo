from django.urls import path
from .import views

urlpatterns=[
    path('users/',views.users),
    path('user/<int:user_id>',views.user_details),
    path('user/chang_password/',views.change_password),
    path('user/login/',views.login_page),
    path('user_detail',views.user_detail)
]
