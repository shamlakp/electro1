from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
 


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )


    def __str__(self):
        return self.name
    
    def get_ancestors(self, include_self=False):
        """
        Recursively fetches all ancestors of the current category.
        """
        ancestors = []
        if include_self:
            ancestors.append(self)
        parent = self.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors[::-1]  # Reverse to get from root to current category

    def get_descendants(self, include_self=False):
        """
        Recursively fetches all descendants of the current category.
        """
        descendants = []
        if include_self:
            descendants.append(self)
        children = self.subcategories.all()  # Updated to match the related_name in parent field
        for child in children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    
User = get_user_model() 
class Product(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg')

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'