# JMD Professionals — Django E-Commerce Website

A full-featured Django sportswear e-commerce website with admin-driven content management.

---

## 🚀 Quick Start

```bash
# 1. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Load demo data (categories, products, steps, admin user)
python manage.py setup_demo

# 5. Start the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin → **admin / admin123**

---

## 🛠️ Admin — What You Can Manage

### Site Settings (1 screen, controls everything)
- **Branding** — Site name, tagline, logo, favicon
- **Colours** — Primary (red), Secondary (navy), Accent (gold) — change the whole theme from hex codes
- **Hero Section** — Heading, subheading, CTA buttons, background image
- **Promo Ticker** — Scrolling announcement bar (pipe-separated items)
- **Stats Bar** — 4 editable stats (numbers + labels)
- **Contact Info** — Phone, WhatsApp, email, address, hours
- **Social Media** — Facebook, Instagram, Twitter, YouTube links
- **SEO** — Meta title, description, keywords
- **Footer** — About text, copyright
- **Catalogue** — PDF upload + banner image

### Categories
- Name, icon (emoji), background colour, eyebrow label
- Toggle show on homepage / in nav
- Drag-to-reorder

### Products
- Name, category, price, sale price
- Up to 3 product images
- Badge (New In / Sale / Combo / Hot)
- Sizes & colours available (comma-separated)
- Featured toggle (shows on homepage)
- Minimum order quantity

### Content
- **Hero Slides** — Multiple hero banners with images and CTAs
- **Announcements** — Ticker bar items with optional links
- **How to Order Steps** — Number, title, description, icon
- **Testimonials** — Client reviews with star ratings
- **Gallery Images** — Masonry gallery with category filtering
- **Contact Messages** — View all form submissions, mark as read
- **Quote Requests** — Track status (New → Contacted → Quoted → Confirmed)

---

## 📁 Project Structure

```
jmdsite/
├── jmd/                    # Django project config
│   ├── settings.py
│   └── urls.py
├── core/                   # Site settings, pages, gallery, contact
│   ├── models.py           # SiteSettings, HeroSlide, Announcement, OrderStep, Testimonial, GalleryImage, ContactMessage
│   ├── admin.py
│   ├── views.py
│   └── urls.py
├── store/                  # Products, categories, cart, quotes
│   ├── models.py           # Category, Product, QuoteRequest
│   ├── admin.py
│   ├── views.py
│   └── urls.py
├── templates/
│   ├── base.html           # Full layout — nav, footer, WhatsApp button
│   ├── home.html           # Homepage
│   ├── gallery.html
│   ├── contact.html
│   ├── how_to_order.html
│   ├── about.html
│   └── shop/
│       ├── shop.html       # Product listing with sidebar
│       ├── category.html   # Category page
│       ├── product_detail.html
│       ├── cart.html
│       └── quote.html
├── static/                 # CSS, JS, images
├── media/                  # Uploaded files (logo, products, gallery)
└── requirements.txt
```

---

## 🎨 Customising Colours

Go to **Admin → Site Settings → Colours** and change:
- `primary_color` — Main brand colour (default: #d62828 red)
- `secondary_color` — Dark background colour (default: #0a1628 navy)
- `accent_color` — Highlight colour (default: #f0a500 gold)

The entire site updates instantly — no code changes needed.

---

## 🌐 Pages

| URL | Page |
|-----|------|
| `/` | Homepage |
| `/shop/` | All Products |
| `/shop/category/<slug>/` | Category Page |
| `/shop/product/<slug>/` | Product Detail |
| `/shop/cart/` | Shopping Cart |
| `/shop/quote/` | Quote Request Form |
| `/how-to-order/` | How to Order |
| `/gallery/` | Photo Gallery |
| `/about/` | About Us |
| `/contact/` | Contact Form |
| `/admin/` | Admin Dashboard |

---

## 📦 Production Checklist

- [ ] Change `SECRET_KEY` in `settings.py`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up proper email backend (not console)
- [ ] Run `python manage.py collectstatic`
- [ ] Set up a proper database (PostgreSQL recommended)
- [ ] Configure media file serving (S3 or similar)
