from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import SalesmanForm
from ..models import Salesman 
from django.contrib import messages

@login_required(login_url='login')
def add_salesman_view(request):
    if request.method == "POST":
        form = SalesmanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salesman added successfully!")
            return redirect('salesman_list')
    else:
        form = SalesmanForm()

    return render(request, 'add_salesman.html', {'form': form})

# New: View Salesmen List
@login_required(login_url='login')
def salesman_list_view(request):
    salesmen = Salesman.objects.all().order_by('-created_at')
    return render(request, 'salesman_list.html', {'salesmen': salesmen ,'admin_name': request.user.username })
@login_required(login_url='login')
def edit_salesman_view(request, id):
    salesman = get_object_or_404(Salesman, id=id)
    if request.method == 'POST':
        form = SalesmanForm(request.POST, instance=salesman)
        if form.is_valid():
            form.save()
            return redirect('salesman_list')
    else:
        form = SalesmanForm(instance=salesman)
    return render(request, 'add_salesman.html', {'form': form})

@login_required(login_url='login')
def delete_salesman_view(request, id):
    salesman = get_object_or_404(Salesman, id=id)
    salesman.delete()
    return redirect('salesman_list')

