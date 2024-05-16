from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
class ClothCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)
    def __iter__(self):
        for cloth in self.clothes.filter(is_visible = True):
            yield cloth
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort',)

class Cloth(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    ]
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('black', 'Black'),
        ('white', 'White'),
        ('yellow', 'Yellow'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('brown', 'Brown'),
        ('orange', 'Orange'),
        ('gray', 'Gray'),
        ('beige', 'Beige'),
    ]
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    MATERIAL_CHOICES = [
        ('cotton', 'Cotton'),
        ('wool', 'Wool'),
        ('polyester', 'Polyester'),
        ('silk', 'Silk'),
        ('leather', 'Leather'),
        ('linen', 'Linen'),
        ('cashmere', 'Cashmere'),
        ('denim', 'Denim'),
        ('velvet', 'Velvet'),
        ('nylon', 'Nylon'),
        ('spandex', 'Spandex'),
        ('acrylic', 'Acrylic'),
        ('rayon', 'Rayon'),
    ]
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    category = models.ForeignKey(ClothCategory, on_delete=models.CASCADE, related_name="cloth")
    genre = models.CharField(max_length=50, choices=GENDER_CHOICES)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    brand = models.CharField(max_length=50)
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    is_visible = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="cloth", blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort',)

class Order(models.Model):
    phone_regex = RegexValidator(regex=r'^\(+38)?\d(9,15)$',
                                 message="Phone number must be entered in the format: '+380509999999'. Up to 15 digits allowed.")

    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[phone_regex])
    comment = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-create_at',)

class CartItem(models.Model):
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.cloth.name} - ${self.total_price}"
