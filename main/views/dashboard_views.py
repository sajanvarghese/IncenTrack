from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Only allow superuser
                login(request, user)
                return redirect('monthly_incentives')  # redirect to dashboard

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'loginpage.html')
@login_required(login_url='login')
def base_view(request):
    """
    Renders the dashboard page.
    - base.html is the main layout and shows dashboard content
    - incentives list empty for now
    """
    return render(request, 'base.html', {
        "admin_name": request.user.username,
        # "incentives": []  # empty list for now
    })
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')
