from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'userApp/register.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')