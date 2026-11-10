# shop/models.py
# Create the data models (tables for the Shopp App)

from django.db import models
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import os

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ("shop:product_list_by_category", args=[self.slug])

def product_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower() # Any image extension ".jpg", ".png"
    return f'products/{instance.id}{ext}'

class OverwriteStorage(FileSystemStorage):
    """Replace an existing file instead of adding a random suffix."""
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to=product_image_path,
        storage=OverwriteStorage(),
        blank=True,
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        # New product: save first so it gets an id, then save the image
        if self.pk is None and self.image:
            image = self.image
            self.image = None
            super().save(*args, **kwargs)
            self.image = image
            kwargs['force_insert'] = False
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug]) # type:ignore


