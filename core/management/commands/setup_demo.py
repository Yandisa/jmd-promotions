from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SiteSettings, OrderStep, Announcement
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Load demo data for JMD Promotions'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@jmd.co.za', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Superuser: admin / admin123'))
        else:
            self.stdout.write('ℹ️  Admin user already exists')

        SiteSettings.get()
        self.stdout.write(self.style.SUCCESS('✅ SiteSettings initialised'))

        if not OrderStep.objects.exists():
            steps = [
                ("01","Choose Your Gear","Browse our catalogue or shop online. Select your styles, colours, and quantities.","⚽",1),
                ("02","Send Your Artwork","Email us your club badge or logo (AI, EPS or high-res PDF) with your preferred colours.","🎨",2),
                ("03","Approve Your Proof","We'll send back a digital mockup. Once you're happy, confirm and pay to proceed.","✅",3),
                ("04","We Deliver","Your fully branded teamwear is finished and couriered directly to you — nationwide.","🚚",4),
            ]
            for num,title,desc,icon,order in steps:
                OrderStep.objects.create(number=num,title=title,description=desc,icon=icon,order=order)
            self.stdout.write(self.style.SUCCESS('✅ How-to-Order steps created'))

        if not Announcement.objects.exists():
            Announcement.objects.create(text="Free Branding on Orders Over R5,000", active=True, order=1)
            Announcement.objects.create(text="2026 Catalogue Now Available", link_text="Download", link_url="#", active=True, order=2)
            Announcement.objects.create(text="Nationwide Delivery | Custom Name & Number Printing | Club & School Packages", active=True, order=3)
            self.stdout.write(self.style.SUCCESS('✅ Announcements created'))

        if not Category.objects.exists():
            cats = [
                ("Combo Specials","⚡","#1a3b18","Best Value",0),
                ("Tracksuits","🏃","#0d2b4a","Training & Travel",1),
                ("Football Kits","⚽","#3b0d0d","Custom Colours",2),
                ("Basketball Kits","🏀","#0d2b1a","Full Team Sets",3),
                ("Training Bibs","🎽","#2b1a0d","Practice Gear",4),
                ("Off-Field Apparel","👟","#1a0d2b","Off the Pitch",5),
                ("Extra Branding","🖨️","#0d1a2b","Names, Numbers & Logos",6),
            ]
            for name,icon,bg,eyebrow,order in cats:
                Category.objects.create(name=name,icon=icon,bg_color=bg,eyebrow=eyebrow,show_on_home=True,order=order)
            self.stdout.write(self.style.SUCCESS('✅ Categories created'))

        if not Product.objects.exists():
            cat_map = {c.name:c for c in Category.objects.all()}
            products = [
                ("Full Football Kit – Shirt, Shorts & Socks","Football Kits",320.00,None,"new",True),
                ("Away Football Kit – Contrast Colours","Football Kits",320.00,280.00,"sale",True),
                ("Micro-Fibre Tracksuit – Top & Bottom","Tracksuits",480.00,None,"new",True),
                ("Fleece-Lined Warm-Up Tracksuit","Tracksuits",560.00,490.00,"sale",False),
                ("Kit + Tracksuit + Bag Combo","Combo Specials",890.00,None,"combo",True),
                ("Football Kit x16 Team Combo","Combo Specials",4500.00,3999.00,"combo",True),
                ("Numbered Training Bibs – Set of 16","Training Bibs",240.00,None,"",False),
                ("Branded Club Hoodie – Fleece Lined","Off-Field Apparel",360.00,None,"new",True),
                ("Reversible Basketball Vest & Shorts","Basketball Kits",295.00,None,"",False),
                ("Custom Cap with Embroidery","Off-Field Apparel",145.00,None,"",False),
            ]
            for name,cat_name,price,sale,badge,featured in products:
                cat = cat_map.get(cat_name)
                if cat:
                    Product.objects.create(
                        name=name,category=cat,price=price,sale_price=sale,
                        badge=badge,featured=featured,active=True,
                        sizes_available="XS,S,M,L,XL,XXL",
                        colours_available="Red,Blue,Black,White,Green,Yellow",
                        stock_note="Made to order",min_qty=1
                    )
            self.stdout.write(self.style.SUCCESS(f'✅ {Product.objects.count()} products created'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Demo data loaded! Visit http://127.0.0.1:8000'))
        self.stdout.write(self.style.SUCCESS('   Admin: http://127.0.0.1:8000/admin  →  admin / admin123'))
