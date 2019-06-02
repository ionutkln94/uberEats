from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Web.forms import UserForm, SupermarketForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return redirect(supermarket_home)

@login_required(login_url='/supermarket/sign-in/')
def supermarket_home(request):
    return render(request, 'supermarket/home.html', {})

def supermarket_sign_up(request):
    user_form1 = UserForm()
    supermarket_form1 = SupermarketForm()

    if request.method == "POST":
        user_form1 = UserForm(request.POST)
        supermarket_form1 = SupermarketForm(request.POST, request.FILES)

        if user_form1.is_valid() and supermarket_form1.is_valid():
            new_user = User.objects.create_user(**user_form1.cleaned_data)
            new_supermarket =  supermarket_form1.save(commit=False) # commit = false - creeaza doar in memorie - nu salveaza datele
            new_supermarket.user = new_user
            new_supermarket.save() # savleaza in memorie

            login(request, authenticate(
                username = user_form1.cleaned_data["username"],
                password = user_form1.cleaned_data["password"]
            ))

            return redirect(supermarket_home)


    return render(request, 'supermarket/sign-up.html', {"user_form":user_form1, "supermarket_form":supermarket_form1})
