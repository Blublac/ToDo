from django.urls import path
from . import views

urlpatterns = [
    path('todos',views.todo_list),
    path('todos/<int:todo_id>',views.todo_details),
    path('todo/completed/', views.completetodo),
    path('todo/incompleted/', views.incompletetodo),
    path('todo/completed/<int:todo_id>',views.mark_complete)
]