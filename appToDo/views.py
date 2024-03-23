from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from .models import Task

# Create your views here.
def welcome(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "pages/welcome.html")

def register_user(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "pages/register.html")
    
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    
    error_message = 0
    # Tentar fazer um dicionário
    username_message_error = ""
    password_message_error = ""
    confirm_password_message_error = ""
    exist_username_message_error = ""
    exist_email_message_error = ""
    
    user_username = User.objects.filter(username=username)
    user_email = User.objects.filter(email=email)
    
    if len(username) < 4:
        username_message_error = "username deve ter no mínimo 4 caracteres."
        error_message += 1
    
    if len(password) < 7:
        password_message_error = "senha muito curta."
        error_message += 1
    
    if password != confirm_password:
        confirm_password_message_error = "senhas diferentes."
        error_message += 1
        
    if user_username.exists():
        exist_username_message_error = "usuário existente."
        error_message += 1
        
    if user_email.exists():
        exist_email_message_error = "email já cadastrado."
        error_message += 1
        
    
    if error_message > 0:
        return render(request, "pages/register.html", {"username_message_error": username_message_error, 
                                                       "password_message_error": password_message_error, 
                                                       "confirm_password_message_error": confirm_password_message_error, 
                                                       "exist_username_message_error": exist_username_message_error, 
                                                       "exist_email_message_error": exist_email_message_error, 
                                                       "user_first_name": first_name, 
                                                       "user_last_name": last_name, 
                                                       "user_username": username, 
                                                       "user_email": email})
    
    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    user.save()

    return redirect("login")

def login_user(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "pages/login.html")
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        messages.warning(request, "usuário ou senha está errado.")
        return redirect("login")
    
def logout_user(request):
    logout(request)
    return redirect("welcome")
    
@login_required
def home(request):
    username=get_user(request)
    if request.method == "POST":
        task = request.POST.get("add-task")
    
        if task == '':
            messages.warning(request, "adicione uma tarefa.") 
            return redirect("home")
        
        current_user = User.objects.get(username=username)
        task = Task(description=task, user=current_user)
        task.save()
    
    all_tasks = Task.objects.filter(user=username)
    context = {"tasks": all_tasks}
    
    return render(request, "pages/home.html", context)

@login_required
def delete_task(request, task_id):
    task = Task.objects.filter(id=task_id)
    task.delete()
    return redirect('home')

@login_required
def delete_all_tasks(request):
    username = get_user(request)
    print(username)
    user = User.objects.get(username=username)
    tasks = Task.objects.filter(user=user)
    print(tasks)
    tasks.delete()
    return redirect('home')
    
    
        
    
