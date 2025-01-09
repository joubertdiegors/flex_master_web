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

class CustomerType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_type_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_type_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer Type"
        verbose_name_plural = "Customer Types"
        ordering = ['name']

    def __str__(self):
        return self.name

class CustomerState(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_state_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_state_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer State"
        verbose_name_plural = "Customer States"
        ordering = ['name']

    def __str__(self):
        return self.name

class Customer(models.Model):
    # Dados automáticos / ao definir o customer_type os inputs serão ajustados para corresponder aos dados que devem ser preenchidos.
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='customer_profile', null=True, blank=True)
    customer_type = models.ForeignKey(CustomerType, on_delete=models.PROTECT, blank=True, null=True)

    # Cadastro de pessoa física
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)  # Campo de data de nascimento

    # Cadastro de empresa
    company_name = models.CharField(max_length=255, blank=True, null=True)
    tva_number = models.CharField(max_length=50, blank=True, null=True)
    contact_person_name = models.CharField(max_length=255, blank=True, null=True)
    contact_person_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_person_email = models.EmailField(blank=True, null=True)
    other_email = models.EmailField(blank=True, null=True)

    # Outros campos
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='customers/images/', blank=True, null=True)
    status = models.ForeignKey(CustomerState, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_created_user', on_delete=models.PROTECT, default=1)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        print("Dados do Customer antes de salvar:", self.__dict__)
        # Normaliza o nome do país
        normalized_name = unidecode(self.first_name).lower().replace(' ', '_')
        image_filename = f"{normalized_name}_photo.webp"

        if self.pk:
            try:
                this = Customer.objects.get(pk=self.pk)

                # Verifica se o campo name foi alterado
                if this.first_name != self.first_name:
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

            except Customer.DoesNotExist:
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
@receiver(pre_save, sender=Customer)
def delete_image_on_clear(sender, instance, **kwargs):
    if instance.pk:
        try:
            this = Customer.objects.get(pk=instance.pk)
            if this.image and not instance.image:
                # Deleta a imagem antiga se o campo de imagem foi limpo
                if os.path.isfile(this.image.path):
                    os.remove(this.image.path)
        except Customer.DoesNotExist:
            pass