from django.db import models
from django.core.exceptions import ValidationError

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="JMD Promotions")
    site_tagline = models.CharField(max_length=200, default="Premium Teamwear & Sportswear")
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#d62828')
    secondary_color = models.CharField(max_length=7, default='#0a1628')
    accent_color = models.CharField(max_length=7, default='#f0a500')
    hero_heading = models.CharField(max_length=200, default="Kit Your Whole Team Out.")
    hero_subheading = models.TextField(default="Custom football kits, tracksuits, training gear and off-field apparel — fully branded with your club colours.")
    hero_cta_text = models.CharField(max_length=50, default="Shop Teamwear")
    hero_cta2_text = models.CharField(max_length=50, default="View 2026 Catalogue")
    hero_cta2_url = models.CharField(max_length=500, blank=True, default="#")
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    ticker_text = models.TextField(default="Free Branding on Orders Over R5,000 | 2026 Catalogue Now Available | Nationwide Delivery | Custom Name & Number Printing | Club & School Packages Available")
    stat1_number = models.CharField(max_length=20, default="800+")
    stat1_label = models.CharField(max_length=50, default="Teams Kitted")
    stat2_number = models.CharField(max_length=20, default="15")
    stat2_label = models.CharField(max_length=50, default="Years Experience")
    stat3_number = models.CharField(max_length=20, default="5 Day")
    stat3_label = models.CharField(max_length=50, default="Avg Turnaround")
    stat4_number = models.CharField(max_length=20, default="100%")
    stat4_label = models.CharField(max_length=50, default="SA Based & Owned")
    phone = models.CharField(max_length=30, default="+27 11 000 0000")
    whatsapp_number = models.CharField(max_length=20, default="27110000000")
    email = models.EmailField(default="info@jmdprofessionals.co.za")
    address = models.CharField(max_length=200, default="Johannesburg, Gauteng, South Africa")
    hours = models.CharField(max_length=100, default="Mon-Fri: 08:00 - 17:00")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    meta_title = models.CharField(max_length=200, default="JMD Promotions - Premium Teamwear & Sportswear")
    meta_description = models.TextField(default="South Africa's trusted custom teamwear specialists.")
    footer_about = models.TextField(default="South Africa's trusted custom teamwear specialists. Serving clubs, schools and academies since 2009 - based in Johannesburg, shipping nationwide.")
    footer_copyright = models.CharField(max_length=200, default="2026 JMD Promotions. All rights reserved.")
    catalogue_pdf = models.FileField(upload_to='catalogues/', blank=True, null=True)
    catalogue_banner = models.ImageField(upload_to='banners/', blank=True, null=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(models.Model):
    heading = models.CharField(max_length=200)
    subheading = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    bg_color = models.CharField(max_length=7, default='#0a1628')
    cta_text = models.CharField(max_length=50, default="Shop Now")
    cta_url = models.CharField(max_length=200, default="/shop/")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Hero Slide"

    def __str__(self):
        return self.heading


class Announcement(models.Model):
    text = models.CharField(max_length=300)
    link_text = models.CharField(max_length=50, blank=True)
    link_url = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:60]


class OrderStep(models.Model):
    number = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="⚽")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "How to Order Step"

    def __str__(self):
        return f"{self.number}. {self.title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    club_or_school = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.club_or_school}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Gallery Image"

    def __str__(self):
        return self.title
