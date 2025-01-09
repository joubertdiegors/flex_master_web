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

class SupplierType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_type_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_type_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Supplier Type"
        verbose_name_plural = "Supplier Types"
        ordering = ['name']

    def __str__(self):
        return self.name

class SupplierState(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_state_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_state_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Supplier State"
        verbose_name_plural = "Supplier States"
        ordering = ['name']

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    supplier_type = models.ForeignKey(SupplierType, on_delete=models.PROTECT, default=0)
    national_number = models.CharField(max_length=50, blank=True, null=True)
    tva_number = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='supplier/images/', blank=True, null=True)
    status = models.ForeignKey(SupplierState, on_delete=models.PROTECT, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Normaliza o nome do país
        normalized_name = unidecode(self.name).lower().replace(' ', '_')
        image_filename = f"{normalized_name}_photo.webp"

        if self.pk:
            try:
                this = Supplier.objects.get(pk=self.pk)

                # Verifica se o campo name foi alterado
                if this.name != self.name:
                    # Caminho antigo da imagem
                    old_image_path = this.image.path if this.image else None

                    # Caminho novo da imagem
                    new_image_path = os.path.join(image_filename)

                    # Renomeia a imagem no sistema de arquivos se o nome do país foi alterado e a imagem não foi alterada
                    if this.image and not self.image:
                        if os.path.isfile(old_image_path):
                            os.rename(old_image_path, os.path.join(this.image.storage.location, new_image_path))
                        self.image.name = new_image_path

                # Verifica se o campo image foi alterado
                if self.image and this.image != self.image:
                    # Deleta a imagem antiga
                    if this.image and os.path.isfile(this.image.path):
                        os.remove(this.image.path)

                    # Processa a nova imagem
                    pil_image = PILImage.open(self.image)
                    output = BytesIO()

                    # Redimensiona mantendo a proporção, com altura máxima de 400px
                    max_height = 400
                    width, height = pil_image.size
                    if height > max_height:
                        new_height = max_height
                        new_width = int((new_height / height) * width)
                        pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

                    pil_image.save(output, format='WebP', quality=85)
                    self.image.file = output
                    self.image.name = os.path.join(image_filename)

            except Supplier.DoesNotExist:
                pass
        else:
            if self.image:
                # Processa a nova imagem para um novo registro
                pil_image = PILImage.open(self.image)
                output = BytesIO()

                # Redimensiona mantendo a proporção, com altura máxima de 400px
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
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

# Sinal de pré-salvamento para deletar a imagem se o campo foi limpo
@receiver(pre_save, sender=Supplier)
def delete_image_on_clear(sender, instance, **kwargs):
    if instance.pk:
        try:
            this = Supplier.objects.get(pk=instance.pk)
            if this.image and not instance.image:
                # Deleta a imagem antiga se o campo de imagem foi limpo
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except Supplier.DoesNotExist:
            pass
