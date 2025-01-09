from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='category_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='category_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_full_path(self):
        category = self
        path = [category.name]
        while category.parent is not None:
            category = category.parent
            path.append(category.name)
        return '/'.join(reversed(path))
    
    # Ajustando o caminho do breadcrumb
    def get_ancestors(self):
        category = self
        ancestors = []
        while category.parent is not None:
            category = category.parent
            ancestors.insert(0, category)
        return ancestors
