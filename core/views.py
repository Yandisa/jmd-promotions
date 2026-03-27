from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SiteSettings, HeroSlide, OrderStep, Testimonial, GalleryImage, ContactMessage
from store.models import Category, Product

def home(request):
    s = SiteSettings.get()

    static_slide = {
        'heading':    s.hero_heading,
        'subheading': s.hero_subheading,
        'cta_text':   s.hero_cta_text,
        'cta_url':    '/shop/',
        'image':      s.hero_image if s.hero_image else None,
        'bg_color':   s.secondary_color,
        'is_static':  True,
    }
    db_slides    = list(HeroSlide.objects.filter(active=True).order_by('order'))
    all_slides   = [static_slide] + db_slides

    # Use 'home_categories' so it does NOT overwrite the global 'categories'
    # that the context processor provides for nav + footer
    home_categories = Category.objects.filter(active=True, show_on_home=True).order_by('order')
    featured        = Product.objects.filter(active=True, featured=True).select_related('category')[:8]
    steps           = OrderStep.objects.filter(active=True)[:4]
    testimonials    = Testimonial.objects.filter(active=True)[:6]
    gallery         = GalleryImage.objects.filter(active=True)[:6]
    ticker_items    = [t.strip() for t in s.ticker_text.split('|') if t.strip()]

    return render(request, 'home.html', {
        'slides':          all_slides,
        'slide_count':     len(all_slides),
        'home_categories': home_categories,   # renamed — only for homepage grid
        'featured':        featured,
        'steps':           steps,
        'testimonials':    testimonials,
        'gallery':         gallery,
        'ticker_items':    ticker_items,
    })

def how_to_order(request):
    steps = OrderStep.objects.filter(active=True)
    return render(request, 'how_to_order.html', {'steps': steps})

def gallery(request):
    images      = GalleryImage.objects.filter(active=True)
    gallery_cats = list(images.values_list('category', flat=True).distinct())
    cat_filter  = request.GET.get('cat', '')
    if cat_filter:
        images = images.filter(category=cat_filter)
    return render(request, 'gallery.html', {'images': images, 'gallery_cats': gallery_cats, 'active_cat': cat_filter})

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, "Thank you! We'll be in touch within 24 hours.")
        return redirect('contact')
    return render(request, 'contact.html')

def about(request):
    s = SiteSettings.get()
    stats = [
        (s.stat1_number, s.stat1_label),
        (s.stat2_number, s.stat2_label),
        (s.stat3_number, s.stat3_label),
        (s.stat4_number, s.stat4_label),
    ]
    return render(request, 'about.html', {'stats': stats})
