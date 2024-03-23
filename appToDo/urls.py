from django.urls import path
from .views import welcome, register_user, login_user, home, logout_user, delete_task, delete_all_tasks

urlpatterns = [
     path('', welcome, name='welcome'), 
     path('register/', register_user, name='register'), 
     path('login/', login_user, name='login'), 
     path('home/', home, name='home'), 
     path('logout/', logout_user, name='logout'), 
     path('delete_task/<task_id>', delete_task, name='delete_task'), 
     path('delete_all_tasks/', delete_all_tasks, name='delete_all_tasks')
]
