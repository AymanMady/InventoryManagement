from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def loginPage(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "There Was An Error, Try Again....")
            return redirect('login')
    else:
        return render(request, "accounts/login.html", context)

def logout_user(request):
    logout(request)
    messages.success(request, ("You were Logged Out!"))
    return redirect('login')