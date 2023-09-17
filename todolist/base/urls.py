from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TaskList.as_view(), name = 'tasks'),

    path('login/', CustomLogInView.as_view(), name = 'login'),
    path('register/', CustomRegistrationView.as_view(), name = 'register'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),

    path('task_create/', TaskCreate.as_view(), name = 'task_create'),
    path('task_delete/<int:pk>/', TaskDelete.as_view(), name = 'task_delete'),
    path('task_update/<int:pk>/', TaskUpdate.as_view(), name = 'task_update'),
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'task'),
]