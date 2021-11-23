from django.urls import path
from . import views

urlpatterns = [
    path('todo', views.todo_list),
    path('todo/<int:todo_id>',views.todo_details),
    # path('books/<int:book_id>',views.book_details),
    # path('cohorts/', views.cohort_list),
]