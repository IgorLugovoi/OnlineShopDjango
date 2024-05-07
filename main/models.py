from django.db import models

# Create your models here.
class ClothCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort',)