from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    
    elif request.method == 'POST':
        email = request.POST['username']  # Treat 'username' as email input
        password = request.POST['password']
        
        # Authenticate using email (by default Django uses 'username')
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            template_data['error'] = 'The email or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')  # Redirect to home page after login

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        
        # Check if the email already exists
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            # If email exists, add an error and re-render the form
            template_data['form'] = form
            template_data['error'] = 'This email is already registered.'
            return render(request, 'accounts/signup.html', {'template_data': template_data})
        
        # If form is valid, save the new user
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.username = user.email  # Set the username to be the email
            user.save()  # Save the user with email as username
            return redirect('accounts.login')  # Redirect to login page after successful signup
        else:
            # If form is not valid, return with form errors
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})
