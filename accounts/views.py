
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AdminRegistrationForm


# Create your views here.
def admin_login(request):
    """
    Handles admin login. Authenticates the user and checks if they are staff.
    If successful, logs in and redirects to the admin dashboard.
    Otherwise, shows an error message.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_staff:
                user.is_staff = True  # Grant admin privileges
                user.save()

            login(request, user)
            return redirect('admin_dashboard')  # Ensure 'dashboard' is a valid URL name

        else:
            messages.error(request, "Invalid credentials or you do not have admin access.")
            print("DEBUG: Login failed")

    return render(request, "accounts/admin_login.html")

def admin_register(request):
    """
    Handles admin registration using AdminRegistrationForm.
    Upon successful registration, marks the user as staff and either redirects to the login page 
    or renders the registration page with a success flag (for popup modal).
    """
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  # Mark the user as an admin.
            user.save()
            messages.success(request, "Registration successful!")
            # Option 1: Redirect to admin login page after registration.
            return redirect('admin_login')
            # Option 2: Render the registration page with a success flag for a popup modal.
            # return render(request, "accounts/register.html", {'registration_success': True})
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = AdminRegistrationForm()
    return render(request, "accounts/admin_register.html", {'form': form})

@login_required
def admin_dashboard(request):
    """Displays the admin dashboard with products belonging to the logged-in admin."""
    
    if not request.user.is_staff:  # Ensure only admin users can access
        return redirect("home")
    # Ensure 'products' is always defined
    products = []
    
    if hasattr(request.user, 'products'):
        products = request.user.products.all()
        reviews = request.user.reviews.all()
    context = {
        'admin': request.user,
        'products': products,
        'reviews': reviews, 
    }
    return render(request, "accounts/admin_dashboard.html", context)

