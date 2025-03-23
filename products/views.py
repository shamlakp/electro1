from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import PublicRegistrationForm, ProductForm, ReviewForm
from .models import Product,Review,Category
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout




# Create your views here.
@login_required
#('accounts.add_product', raise_exception=True)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.admin = request.user
            product.save()
            return redirect('admin_dashboard')  # Redirect to admin dashboard
    else:
        form = ProductForm()
    categories =Category.objects.all()
    return render(request, 'products/add_product.html', {
        'form': form  
    })





def public_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            # For public login, you might not need to check is_staff.
            login(request, user)
            return redirect('profile')  # Redirect to public profile page
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'products/public_login.html')
   
def public_register(request):
    if request.method == 'POST':
        form = PublicRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This creates the new public user
            messages.success(request, "Registration successful! Please log in.")
            # Optionally, you could log the user in automatically:
            # login(request, user)
            # return redirect('profile')
            return redirect('public_login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = PublicRegistrationForm()
    return render(request, 'products/register.html', {'form': form})


def product_list(request):
    products = Product.objects.all()  # Show all products from all admins
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def profile(request):
    user_reviews = Review.objects.filter(user=request.user)
    context = {
        'user_reviews': user_reviews,
    }
    return render(request, 'products/profile.html', context)



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)  # Get all reviews for this product

    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('product_detail', product_id=product.id)  # Refresh page after submission
        else:
            return redirect('public_login')  # Redirect to login if user is not logged in
    else:
        form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })

def get_category_hierarchy(category):
    hierarchy = {'category': category, 'subcategories': []}
    subcategories = category.objects.filter(parent=category)
    for subcategory in subcategories:
        hierarchy['subcategories'].append(get_category_hierarchy(subcategory))
    return hierarchy




def category_list_view(request):
    top_level_categories = Category.objects.filter(parent__isnull=True)
    categories_hierarchy = [get_category_hierarchy(cat) for cat in top_level_categories]
    return render(request, 'add_product.html', {'categories_hierarchy': categories_hierarchy})

def logout(request):
    if request.method == "POST":  # Ensure logout is done via POST
        logout(request)
        return redirect("home")  # Redirect to home after logout

    return redirect("home")    #

def delete_account(request):
    if request.user.is_authenticated:
        request.user.delete()
        return redirect('home')  # Redirect to home after deletion
    return redirect('login')

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect after saving
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/edit_product.html', {'form': form})
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Ensure only the admin who added the product can delete it
    if request.user != product.admin_user and not request.user.is_superuser:
        return redirect('admin_dashboard')  # Redirect if user is not authorized

    if request.method == "POST":
        product.delete()
        return redirect('admin_dashboard')  # Redirect after deletion

    return render(request, 'product/delete_product.html', {'product': product})



