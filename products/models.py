from django.conf import settings
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from PIL import Image as PILImage
from io import BytesIO
from unidecode import unidecode

from branches.models import Country
from categories.models import Category

#Esta tabela armazena a unidade de medida para a venda do produto, se é a peça, ao kg, ao litro e etc...
class SalesUnit(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    is_fractional = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sales_unit_created_user', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sales_unit_updated_user', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.symbol})"

#Esta tabela armazena a unidade de medida para o volume do produto (300g, 300ml, 3L) retornará no detalhe do produto.
class PackageUnit(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='package_unit_created_user', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='package_unit_updated_user', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brands/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='brands_created_user', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='brands_updated_user', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        normalized_name = unidecode(self.name).lower().replace(' ', '_')
        image_filename = f"{normalized_name}_logo.webp"

        if self.pk:
            try:
                this = Brand.objects.get(pk=self.pk)
                if this.name != self.name:
                    old_image_path = this.image.path if this.image else None
                    new_image_path = os.path.join(image_filename)
                    if this.image and not self.image:
                        if os.path.isfile(old_image_path):
                            os.rename(old_image_path, os.path.join(this.image.storage.location, new_image_path))
                        self.image.name = new_image_path

                if self.image and this.image != self.image:
                    if this.image and os.path.isfile(this.image.path):
                        os.remove(this.image.path)
                    pil_image = PILImage.open(self.image)
                    output = BytesIO()
                    max_height = 400
                    width, height = pil_image.size
                    if height > max_height:
                        new_height = max_height
                        new_width = int((new_height / height) * width)
                        pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)
                    pil_image.save(output, format='WebP', quality=85)
                    self.image.file = output
                    self.image.name = os.path.join(image_filename)
            except Brand.DoesNotExist:
                pass
        else:
            if self.image:
                pil_image = PILImage.open(self.image)
                output = BytesIO()
                max_height = 400
                width, height = pil_image.size
                if height > max_height:
                    new_height = max_height
                    new_width = int((new_height / height) * width)
                    pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)
                pil_image.save(output, format='WebP', quality=85)
                self.image.file = output
                self.image.name = os.path.join(image_filename)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

@receiver(pre_save, sender=Brand)
def delete_image_on_clear(sender, instance, **kwargs):
    if instance.pk:
        try:
            this = Brand.objects.get(pk=instance.pk)
            if this.image and not instance.image:
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except Brand.DoesNotExist:
            pass


class Product(models.Model):
    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    volume = models.CharField(max_length=10, null=True, blank=True)
    package_unit = models.ForeignKey(PackageUnit, on_delete=models.PROTECT, related_name='products_package_unit', null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products_brand')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True, related_name='products_country')
    category = models.ManyToManyField(Category, related_name='products_category', blank=True)
    sales_unit = models.ForeignKey(SalesUnit, on_delete=models.PROTECT, null=True, blank=True, related_name='products_sales_unit')
    net_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    stock_control = models.BooleanField(default=True)
    minimum_stock = models.PositiveIntegerField(null=True, blank=True)
    maximum_stock = models.PositiveIntegerField(null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        normalized_name = unidecode(self.name).lower().replace(' ', '_')
        image_filename = f"{normalized_name}_photo.webp"

        if self.pk:
            try:
                this = Product.objects.get(pk=self.pk)
                if this.name != self.name:
                    old_image_path = this.image.path if this.image else None
                    new_image_path = os.path.join(image_filename)
                    if this.image and not self.image:
                        if os.path.isfile(old_image_path):
                            os.rename(old_image_path, os.path.join(this.image.storage.location, new_image_path))
                        self.image.name = new_image_path

                if self.image and this.image != self.image:
                    if this.image and os.path.isfile(this.image.path):
                        os.remove(this.image.path)
                    pil_image = PILImage.open(self.image)
                    output = BytesIO()
                    max_height = 500
                    width, height = pil_image.size
                    if height > max_height:
                        new_height = max_height
                        new_width = int((new_height / height) * width)
                        pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)
                    pil_image.save(output, format='WebP', quality=85)
                    self.image.file = output
                    self.image.name = os.path.join(image_filename)
            except Product.DoesNotExist:
                pass
        else:
            if self.image:
                pil_image = PILImage.open(self.image)
                output = BytesIO()
                max_height = 500
                width, height = pil_image.size
                if height > max_height:
                    new_height = max_height
                    new_width = int((new_height / height) * width)
                    pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)
                pil_image.save(output, format='WebP', quality=85)
                self.image.file = output
                self.image.name = os.path.join(image_filename)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

@receiver(pre_save, sender=Product)
def delete_image_on_clear(sender, instance, **kwargs):
    if instance.pk:
        try:
            this = Product.objects.get(pk=instance.pk)
            if this.image and not instance.image:
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except Product.DoesNotExist:
            pass

# Ingredientes e tabela nutricional, vai ser apresentado dentro dos detalhes do produto.
class Ingredients(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='ingredients_product')
    ingredients = models.TextField()  # Ingredientes
    allergens = models.TextField(blank=True, null=True)  # Alergênicos
    conservation_instructions = models.TextField(blank=True, null=True)  # Instruções para conservação

    class Meta:
        ordering = ['product']

    def __str__(self):
        return self.product.name

class NutritionalItem(models.Model):
    name = models.CharField(max_length=100)  # Nome do item nutricional (ex: Carboidrato, Proteína)
    package_unit = models.ForeignKey(PackageUnit, related_name='nutritional_item_package_unit', on_delete=models.PROTECT, null=True, blank=True)  # Unidade de medida

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class NutritionalInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='nutritional_info_product')
    nutritional_item = models.ForeignKey(NutritionalItem, on_delete=models.CASCADE, related_name='nutritional_info_nutritional_item')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Quantidade do item nutricional

    class Meta:
        unique_together = ('product', 'nutritional_item')
        ordering = ['product', 'nutritional_item']

    def __str__(self):
        return self.product.name
