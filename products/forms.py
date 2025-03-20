from django import forms
from .models import Product,Category
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Select a category',
        widget=forms.Select(attrs={'class': 'form-control'}),
      
    )

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'image']
        
class PublicRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']