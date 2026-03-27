from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, default='', help_text='Optional Font Awesome class e.g. fa-futbol')
    bg_color = models.CharField(max_length=7, default='#0d2b4a')
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    show_on_home = models.BooleanField(default=True)
    eyebrow = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Categories"

    def __str__(self): return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category_detail', args=[self.slug])


class Product(models.Model):
    BADGE_CHOICES = [('','None'),('new','New In'),('sale','Sale'),('combo','Combo'),('hot','Hot')]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    badge = models.CharField(max_length=10, choices=BADGE_CHOICES, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    includes_branding = models.BooleanField(default=False)
    min_qty = models.PositiveIntegerField(default=1)
    sizes_available = models.CharField(max_length=200, blank=True, help_text='e.g. XS,S,M,L,XL,XXL')
    colours_available = models.CharField(max_length=300, blank=True, help_text='e.g. Red,Blue,Black')
    stock_note = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created']

    def __str__(self): return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', args=[self.slug])

    @property
    def display_price(self):
        return self.sale_price if self.sale_price else self.price

    @property
    def sizes_list(self):
        return [s.strip() for s in self.sizes_available.split(',') if s.strip()]

    @property
    def colours_list(self):
        return [c.strip() for c in self.colours_available.split(',') if c.strip()]


class QuoteRequest(models.Model):
    STATUS = [('new','New'),('contacted','Contacted'),('quoted','Quoted'),('confirmed','Confirmed'),('closed','Closed')]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    club_name = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    sizes_breakdown = models.TextField(blank=True)
    colours = models.CharField(max_length=200, blank=True)
    branding_details = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='new')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} – {self.product or 'General'} x{self.quantity}"
