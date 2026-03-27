from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, QuoteRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'bg_color_preview', 'order', 'active', 'show_on_home', 'product_count')
    list_editable = ('order', 'active', 'show_on_home')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def bg_color_preview(self, obj):
        return format_html('<span style="background:{};padding:4px 14px;border-radius:3px;color:#fff;font-size:11px;">{}</span>', obj.bg_color, obj.bg_color)
    bg_color_preview.short_description = "Colour"

    def product_count(self, obj):
        count = obj.products.filter(active=True).count()
        return format_html('<b>{}</b>', count)
    product_count.short_description = "Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price_display', 'badge', 'featured', 'active', 'order')
    list_editable = ('featured', 'active', 'order')
    list_display_links = ('name',)
    list_filter = ('category', 'active', 'featured', 'badge')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Product Info', {'fields': ('category', 'name', 'slug', 'description')}),
        ('Pricing', {'fields': ('price', 'sale_price')}),
        ('Images', {'fields': ('image', 'image2', 'image3')}),
        ('Options', {'fields': ('sizes_available', 'colours_available', 'min_qty', 'includes_branding', 'stock_note')}),
        ('Display', {'fields': ('badge', 'featured', 'active', 'order')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px;width:45px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return format_html('<div style="width:45px;height:45px;background:{};border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:18px;">{}</div>', obj.category.bg_color, obj.category.icon)
    image_preview.short_description = ""

    def price_display(self, obj):
        if obj.sale_price:
            return format_html('<span style="text-decoration:line-through;color:#aaa;">R{}</span> <b style="color:#d62828;">R{}</b>', obj.price, obj.sale_price)
        return format_html('R{}', obj.price)
    price_display.short_description = "Price"


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'club_name', 'product', 'quantity', 'status', 'created')
    list_editable = ('status',)
    list_filter = ('status',)
    readonly_fields = ('name','email','phone','club_name','product','quantity','sizes_breakdown','colours','branding_details','notes','created')
    search_fields = ('name', 'email', 'club_name')

    def has_add_permission(self, request): return False
