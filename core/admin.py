from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, HeroSlide, Announcement, OrderStep, Testimonial, ContactMessage, GalleryImage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Branding', {'fields': ('site_name', 'site_tagline', 'logo', 'favicon')}),
        ('Colours', {'fields': ('primary_color', 'secondary_color', 'accent_color'), 'description': 'Use hex codes e.g. #d62828'}),
        ('Hero Section', {'fields': ('hero_heading', 'hero_subheading', 'hero_cta_text', 'hero_cta2_text', 'hero_cta2_url', 'hero_image')}),
        ('Promo Ticker', {'fields': ('ticker_text',), 'description': 'Separate items with | character'}),
        ('Stats Bar', {'fields': (('stat1_number','stat1_label'),('stat2_number','stat2_label'),('stat3_number','stat3_label'),('stat4_number','stat4_label'),)}),
        ('Contact Info', {'fields': ('phone', 'whatsapp_number', 'email', 'address', 'hours')}),
        ('Social Media', {'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url')}),
        ('SEO', {'fields': ('meta_title', 'meta_description'), 'classes': ('collapse',)}),
        ('Footer', {'fields': ('footer_about', 'footer_copyright')}),
        ('Catalogue', {'fields': ('catalogue_pdf', 'catalogue_banner')}),
    )
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('heading', 'cta_text', 'order', 'active', 'preview')
    list_editable = ('order', 'active')
    list_display_links = ('heading',)
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url)
        return format_html('<span style="background:{};padding:4px 10px;color:#fff;border-radius:3px;font-size:11px;">{}</span>', obj.bg_color, obj.bg_color)
    preview.short_description = "Preview"

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('text', 'active', 'order')
    list_editable = ('active', 'order')

@admin.register(OrderStep)
class OrderStepAdmin(admin.ModelAdmin):
    list_display = ('number', 'icon', 'title', 'order', 'active')
    list_editable = ('order', 'active')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'club_or_school', 'rating', 'active')
    list_editable = ('active',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created', 'read')
    list_editable = ('read',)
    list_filter = ('read',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created')
    def has_add_permission(self, request): return False

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'active', 'preview')
    list_editable = ('order', 'active', 'category')
    list_display_links = ('title',)
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;object-fit:cover;">', obj.image.url)
        return "—"
    preview.short_description = "Preview"
