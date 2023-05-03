from django.shortcuts import render, redirect



def home(request):

    return render(request, 'home.html')



def login_with_google(request):
    if not request.user.is_authenticated:
        return redirect('social:begin', 'google-oauth2')
    else:
        return redirect('home')