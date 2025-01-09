from django.conf import settings
import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PILImage
from io import BytesIO
from unidecode import unidecode
from django.dispatch import receiver
from django.db.models.signals import pre_save

from products.models import Brand, Product

class GlobalSettings(models.Model):
    site_under_maintenance = models.BooleanField(default=False, verbose_name="Site em manutenção")
    maintenance_message = models.TextField(
        default="Estamos em manutenção. Voltaremos em breve!",
        verbose_name="Mensagem de manutenção",
    )    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='maintenance_created_by', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Criado por")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='maintenance_updated_by', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Atualizado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return "Configurações Globais"

class Banner(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField()
    link = models.URLField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='banner_created_user', null=True, blank=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='banner_updated_user', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ajustando o nome do banner
        normalized_name = unidecode(self.title).lower().replace(' ', '_')
        image_filename = f"{normalized_name}.webp"

        if self.pk:
            try:
                this = Banner.objects.get(pk=self.pk)

                # Verifica se o campo name foi alterado
                if this.title != self.title:
                    # Caminho antigo da imagem
                    old_image_path = this.image.path if this.image else None

                    # Caminho novo da imagem
                    new_image_path = os.path.join('banners/', image_filename)

                    # Renomeia a imagem no sistema de arquivos se o nome da marca foi alterado e a imagem não foi alterada
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
                    max_height = 200
                    width, height = pil_image.size
                    if height > max_height:
                        new_height = max_height
                        new_width = int((new_height / height) * width)
                        pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

                    pil_image.save(output, format='WebP', quality=85)
                    self.image.file = output
                    self.image.name = os.path.join('banners/', image_filename)

            except Banner.DoesNotExist:
                pass
        else:
            if self.image:
                # Processa a nova imagem para um novo registro
                pil_image = PILImage.open(self.image)
                output = BytesIO()

                # Redimensiona mantendo a proporção, com altura máxima de 400px
                max_height = 335
                width, height = pil_image.size
                if height > max_height:
                    new_height = max_height
                    new_width = int((new_height / height) * width)
                    pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

                pil_image.save(output, format='WebP', quality=85)
                self.image.file = output
                self.image.name = os.path.join('banners/', image_filename)

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

# Sinal de pré-salvamento para deletar a imagem se o campo foi limpo
@receiver(pre_save, sender=Banner)
def delete_image_on_clear(sender, instance, **kwargs):
    if instance.pk:
        try:
            this = Banner.objects.get(pk=instance.pk)
            if this.image and not instance.image:
                # Deleta a imagem antiga se o campo de imagem foi limpo
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except Banner.DoesNotExist:
            pass


# Produtos mais vendidos
class BestSellerProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='best_seller_product')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='best_seller_created', on_delete=models.PROTECT)

    def __str__(self):
        return self.product.name

# Produtos lançamentos
class FreshProducts(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='fresh_product_product')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fresh_product_created', on_delete=models.PROTECT)

    def __str__(self):
        return self.product.name

# Marcas em destaque
class HighlightedBrand(models.Model):
    brand = models.OneToOneField(Brand, on_delete=models.PROTECT, related_name='custom_brand')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='custom_brand_created', on_delete=models.PROTECT)

    def __str__(self):
        return self.brand.name
