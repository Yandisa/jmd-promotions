from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from urllib.parse import quote as url_quote
from .models import Category, Product, QuoteRequest

def shop(request):
    categories = Category.objects.filter(active=True)
    products   = Product.objects.filter(active=True)
    cat_slug   = request.GET.get('cat', '')
    search     = request.GET.get('q', '')
    sort       = request.GET.get('sort', '')
    active_cat = None
    if cat_slug:
        active_cat = get_object_or_404(Category, slug=cat_slug)
        products   = products.filter(category=active_cat)
    if search:
        products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
    if sort == 'price_asc':   products = products.order_by('price')
    elif sort == 'price_desc': products = products.order_by('-price')
    elif sort == 'newest':     products = products.order_by('-created')
    return render(request, 'shop/shop.html', {
        'categories': categories, 'products': products,
        'active_cat': active_cat, 'search': search, 'sort': sort,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, active=True)
    products  = category.products.filter(active=True)
    sort      = request.GET.get('sort', '')
    if sort == 'price_asc':    products = products.order_by('price')
    elif sort == 'price_desc': products = products.order_by('-price')
    elif sort == 'newest':     products = products.order_by('-created')
    return render(request, 'shop/category.html', {
        'category': category, 'products': products, 'sort': sort,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    related = Product.objects.filter(category=product.category, active=True).exclude(pk=product.pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product, 'related': related,
    })

def _build_cart_items(request):
    """Helper: resolve session cart into list of dicts with product objects."""
    cart_data = request.session.get('cart', {})
    items = []
    total = 0
    for pid, item in cart_data.items():
        try:
            product  = Product.objects.select_related('category').get(pk=pid)
            qty      = item.get('qty', 1)
            subtotal = float(product.display_price) * qty
            total   += subtotal
            items.append({
                'product':  product,
                'qty':      qty,
                'size':     item.get('size', ''),
                'colour':   item.get('colour', ''),
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            pass
    return items, round(total, 2)

def cart(request):
    items, total = _build_cart_items(request)

    # Build WhatsApp message with full cart details
    wa_lines = ["Hi JMD Promotions, I'd like to place an order:\n"]
    for i, item in enumerate(items, 1):
        line = f"{i}. {item['product'].name} x{item['qty']}"
        if item['size']:   line += f" | Size: {item['size']}"
        if item['colour']: line += f" | Colour: {item['colour']}"
        line += f" — R{item['subtotal']:.2f}"
        wa_lines.append(line)
    wa_lines.append(f"\nEstimated total: R{total:.2f} (excl. VAT)")
    wa_lines.append("\nPlease contact me to confirm sizes, branding and payment.")
    wa_message = url_quote("\n".join(wa_lines))

    return render(request, 'shop/cart.html', {
        'items':          items,
        'total':          total,
        'wa_message':     wa_message,
        'default_sizes':  ['XS','S','M','L','XL','XXL','XXXL','Mixed/TBC'],
        'default_colours':['Red','Blue','Black','White','Green','Yellow','Navy','Orange','Purple','Custom/TBC'],
    })

def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    cart    = request.session.get('cart', {})
    qty     = int(request.POST.get('qty', 1))
    size    = request.POST.get('size', '')
    colour  = request.POST.get('colour', '')
    key     = str(product_id)
    if key in cart:
        cart[key]['qty'] += qty
    else:
        cart[key] = {'qty': qty, 'size': size, 'colour': colour}
    request.session['cart']     = cart
    request.session.modified    = True
    messages.success(request, f'"{product.name}" added to your cart.')
    return redirect(request.POST.get('next', 'cart'))

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart']  = cart
    request.session.modified = True
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

def cart_update(request):
    cart = request.session.get('cart', {})
    for key in list(cart.keys()):
        # Update qty
        qty_val = request.POST.get(f'qty_{key}', '')
        if qty_val:
            try:
                qty = int(qty_val)
                if qty < 1:
                    del cart[key]
                    continue
                else:
                    cart[key]['qty'] = qty
            except ValueError:
                pass
        # Update size and colour from inline cart selects
        size_val   = request.POST.get(f'size_{key}', '')
        colour_val = request.POST.get(f'colour_{key}', '')
        if size_val:   cart[key]['size']   = size_val
        if colour_val: cart[key]['colour'] = colour_val
    request.session['cart']  = cart
    request.session.modified = True
    messages.success(request, 'Cart updated.')
    return redirect('cart')

def quote_request(request, product_id=None):
    """
    Quote form — pre-fills from cart session automatically.
    If product_id given (from product page), that product is highlighted.
    """
    # Resolve cart items for pre-fill
    cart_items, cart_total = _build_cart_items(request)

    # Build pre-filled text fields from cart
    cart_sizes_text   = ""
    cart_colours_text = ""
    cart_notes_lines  = []
    if cart_items:
        for item in cart_items:
            line = f"{item['product'].name} x{item['qty']}"
            if item['size']:   line += f" (Size: {item['size']})"
            if item['colour']: line += f" (Colour: {item['colour']})"
            cart_notes_lines.append(line)
        sizes_set   = {i['size'] for i in cart_items if i['size']}
        colours_set = {i['colour'] for i in cart_items if i['colour']}
        if sizes_set:   cart_sizes_text   = ", ".join(sizes_set)
        if colours_set: cart_colours_text = ", ".join(colours_set)

    cart_notes_prefill = "\n".join(cart_notes_lines)
    cart_total_display = f"R{cart_total:.2f}" if cart_total else ""

    # Specific product linked from product detail page
    linked_product = None
    if product_id:
        linked_product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        QuoteRequest.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            club_name=request.POST.get('club_name', ''),
            product=linked_product,
            quantity=int(request.POST.get('quantity') or 1),
            sizes_breakdown=request.POST.get('sizes_breakdown', ''),
            colours=request.POST.get('colours', ''),
            branding_details=request.POST.get('branding_details', ''),
            notes=request.POST.get('notes', ''),
        )
        # Clear the cart after a successful quote submission
        request.session['cart']  = {}
        request.session.modified = True
        messages.success(request, "Quote request submitted! We'll get back to you within 48 hours. Your cart has been cleared.")
        return redirect('home')

    # Build WA message for the quote page's WhatsApp button too
    wa_lines = ["Hi JMD Promotions, I'd like to request a quote:\n"]
    for i, item in enumerate(cart_items, 1):
        line = f"{i}. {item['product'].name} x{item['qty']}"
        if item['size']:   line += f" | Size: {item['size']}"
        if item['colour']: line += f" | Colour: {item['colour']}"
        line += f" — R{item['subtotal']:.2f}"
        wa_lines.append(line)
    if cart_total_display:
        wa_lines.append(f"\nEstimated total: {cart_total_display} (excl. VAT)")
    wa_lines.append("\nPlease contact me to confirm sizes, branding and payment.")
    wa_message = url_quote("\n".join(wa_lines)) if cart_items else ""

    all_products = Product.objects.filter(active=True).order_by('category__name', 'name')
    return render(request, 'shop/quote.html', {
        'linked_product':    linked_product,
        'all_products':      all_products,
        'cart_items':        cart_items,
        'cart_total':        cart_total_display,
        'cart_sizes_prefill':   cart_sizes_text,
        'cart_colours_prefill': cart_colours_text,
        'cart_notes_prefill':   cart_notes_prefill,
        'wa_message':           wa_message,
    })
