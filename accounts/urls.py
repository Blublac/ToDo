from django.urls import path
from .import views

urlpatterns=[
    path('signup',views.signup),
    path('users/',views.users),
    path('user/profile',views.user_profile),
    path('user/chang_password/',views.change_password),
    path('login/',views.login_page),
    path('user_detail/<uuid:user_id>',views.user_detail),
    path('users/nonstaff/',views.nonstaff),
    path('users/staff/',views.staff)
]
