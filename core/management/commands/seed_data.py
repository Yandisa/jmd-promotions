from django.core.management.base import BaseCommand
from core.models import SiteSettings, OrderStep, Testimonial, Announcement
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Seed initial demo data'

    def handle(self, *args, **kwargs):
        # Site settings
        s = SiteSettings.get()
        s.site_name = "JMD Promotions"
        s.site_tagline = "Premium Teamwear & Sportswear"
        s.phone = "+27 11 000 0000"
        s.whatsapp_number = "27110000000"
        s.email = "info@jmdprofessionals.co.za"
        s.address = "Johannesburg, Gauteng, South Africa"
        s.hours = "Mon-Fri: 08:00 - 17:00"
        s.save()
        self.stdout.write('✅ Site settings done')

        # Announcements
        Announcement.objects.get_or_create(
            text="🎉 2026 Collection is now live — Free branding on orders over R5,000!",
            defaults={'active': True, 'order': 1}
        )

        # Categories
        cats = [
            {'name': 'Combo Specials', 'icon': '⚡', 'bg_color': '#0d3b5e', 'eyebrow': 'Best Value', 'order': 1},
            {'name': 'Tracksuits', 'icon': '🏃', 'bg_color': '#3b0d0d', 'eyebrow': 'Training & Travel', 'order': 2},
            {'name': 'Football Kits', 'icon': '⚽', 'bg_color': '#0d3b1a', 'eyebrow': 'Custom Colours', 'order': 3},
            {'name': 'Basketball Kits', 'icon': '🏀', 'bg_color': '#2b1a0d', 'eyebrow': 'All Sports', 'order': 4},
            {'name': 'Training Bibs', 'icon': '🎽', 'bg_color': '#1a0d3b', 'eyebrow': 'Team Training', 'order': 5},
            {'name': 'Off-Field Apparel', 'icon': '👟', 'bg_color': '#0d2b3b', 'eyebrow': 'Off the Pitch', 'order': 6},
            {'name': 'Extra Branding', 'icon': '🖨️', 'bg_color': '#1a3b0d', 'eyebrow': 'Names & Numbers', 'order': 7},
        ]
        cat_objs = {}
        for c in cats:
            obj, _ = Category.objects.get_or_create(name=c['name'], defaults={**c, 'active': True, 'show_on_home': True})
            cat_objs[c['name']] = obj
        self.stdout.write('✅ Categories done')

        # Products
        products = [
            {'name': 'Full Football Kit – Shirt, Shorts & Socks', 'category': 'Football Kits', 'price': 320, 'badge': 'new', 'featured': True, 'min_qty': 10, 'sizes_available': 'XS,S,M,L,XL,XXL', 'colours_available': 'Red/White,Blue/White,Green/Black,Any Custom', 'stock_note': 'Made to order', 'description': 'Complete football kit including custom printed shirt, shorts, and socks. Available in any colour combination with full sublimation printing.'},
            {'name': 'Micro-Fibre Tracksuit Top & Bottom', 'category': 'Tracksuits', 'price': 480, 'sale_price': 420, 'badge': 'sale', 'featured': True, 'min_qty': 5, 'sizes_available': 'XS,S,M,L,XL,XXL,XXXL', 'colours_available': 'Navy/Gold,Black/Red,Royal Blue/White', 'stock_note': 'Made to order', 'description': 'Premium micro-fibre tracksuit with embroidered club badge and player name. Lightweight, breathable, and smart for travel days.'},
            {'name': 'Kit + Tracksuit + Bag Combo Package', 'category': 'Combo Specials', 'price': 890, 'badge': 'combo', 'featured': True, 'min_qty': 10, 'sizes_available': 'XS,S,M,L,XL,XXL', 'colours_available': 'Custom', 'stock_note': 'Made to order', 'description': 'Full combo package including football kit, tracksuit, and kit bag — all branded with your club logo. Our most popular package for clubs.', 'includes_branding': True},
            {'name': 'Numbered Training Bibs – Set of 16', 'category': 'Training Bibs', 'price': 240, 'featured': True, 'min_qty': 1, 'sizes_available': 'One Size', 'colours_available': 'Bibs Yellow,Bibs Orange,Bibs Red,Bibs Green,Bibs Blue', 'description': 'High-visibility training bibs with numbers 1–16. Mesh construction for breathability. Available in multiple colours.'},
            {'name': 'Branded Club Hoodie – Fleece Lined', 'category': 'Off-Field Apparel', 'price': 360, 'badge': 'new', 'featured': True, 'min_qty': 5, 'sizes_available': 'XS,S,M,L,XL,XXL', 'colours_available': 'Navy,Black,Grey,Royal Blue', 'description': 'Premium fleece-lined hoodie with embroidered club badge. Perfect for matchday warmups and travel. Anti-pilling fabric.'},
            {'name': 'Reversible Basketball Vest & Shorts', 'category': 'Basketball Kits', 'price': 295, 'featured': True, 'min_qty': 10, 'sizes_available': 'XS,S,M,L,XL,XXL', 'colours_available': 'Home/Away Custom', 'stock_note': 'Made to order', 'description': 'Reversible basketball kit — home and away in one. Sublimation printed with player name and number on both sides.'},
            {'name': 'Polo Shirt – Pique Cotton', 'category': 'Off-Field Apparel', 'price': 185, 'min_qty': 12, 'sizes_available': 'XS,S,M,L,XL,XXL', 'colours_available': 'White,Navy,Black,Red,Royal Blue,Green,Grey', 'description': 'Classic pique cotton polo shirt with embroidered logo on the left chest. Smart casual wear for club officials and staff.'},
            {'name': 'Club Kit Bag – Large', 'category': 'Extra Branding', 'price': 220, 'min_qty': 1, 'sizes_available': 'One Size', 'colours_available': 'Navy,Black,Red', 'description': 'Large kit bag with separate boot compartment. Custom printed or embroidered with your club name and badge.'},
        ]
        for p in products:
            cat_name = p.pop('category')
            cat = cat_objs.get(cat_name)
            if cat:
                Product.objects.get_or_create(name=p['name'], defaults={**p, 'category': cat, 'active': True})
        self.stdout.write('✅ Products done')

        # Steps
        steps = [
            {'number': '01', 'title': 'Choose Your Gear', 'description': 'Browse our online shop or download our 2026 catalogue. Select your styles, colours, and quantities for your team.', 'icon': '⚽', 'order': 1},
            {'number': '02', 'title': 'Send Your Artwork', 'description': 'Email your club badge or logo in AI, EPS, or high-res PDF format along with your preferred colours and branding requirements.', 'icon': '🎨', 'order': 2},
            {'number': '03', 'title': 'Approve Your Proof', 'description': 'We send a digital mockup of your order for approval. Once you give the green light, you confirm and make payment.', 'icon': '✅', 'order': 3},
            {'number': '04', 'title': 'We Deliver', 'description': 'Your fully branded teamwear is professionally finished and couriered directly to your door — anywhere in South Africa.', 'icon': '🚚', 'order': 4},
        ]
        for step in steps:
            OrderStep.objects.get_or_create(number=step['number'], defaults={**step, 'active': True})
        self.stdout.write('✅ Order steps done')

        # Testimonials
        testimonials = [
            {'name': 'Thabo Mokoena', 'club_or_school': 'Soweto United FC', 'text': 'Absolutely brilliant service! Our kits arrived within a week and the quality is outstanding. The whole squad is buzzing. Will definitely order again!', 'rating': 5},
            {'name': 'Sarah van der Berg', 'club_or_school': 'Pretoria Girls High School', 'text': 'JMD handled our full netball and athletics order. Professional from start to finish — the digital proofs were spot on and the delivery was right on time.', 'rating': 5},
            {'name': 'Coach Sipho Dlamini', 'club_or_school': 'Durban Academy FC', 'text': 'We needed 30 tracksuits in under 2 weeks and they delivered! Great communication, great quality, and fair pricing. Our go-to for all teamwear now.', 'rating': 5},
        ]
        for t in testimonials:
            Testimonial.objects.get_or_create(name=t['name'], defaults={**t, 'active': True})
        self.stdout.write('✅ Testimonials done')
        self.stdout.write(self.style.SUCCESS('\n🎉 All demo data seeded successfully!'))
