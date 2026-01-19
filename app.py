from flask import Flask, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'sneakvault-secret-key-123'

# --- DATABASE (Updated for Capital 'I' in Images) ---
products = [
    # HERO ITEM
    {"id": 4, "name": "Jordan 1 High 'Chicago'", "brand": "JORDAN", "price": "₹38,000", "price_raw": 38000, "image": "/static/Images/chicago.jpg", "size": "US 8", "type": "non-veg"},
    
    # NIKE
    {"id": 1, "name": "Dunk Low 'Panda'", "brand": "NIKE", "price": "₹12,499", "price_raw": 12499, "image": "/static/Images/panda.jpg", "size": "US 10", "type": "non-veg"},
    {"id": 2, "name": "Air Force 1 '07", "brand": "NIKE", "price": "₹8,995", "price_raw": 8995, "image": "/static/Images/af1.jpg", "size": "US 9", "type": "non-veg"},
    {"id": 5, "name": "Blazer Mid '77", "brand": "NIKE", "price": "₹9,695", "price_raw": 9695, "image": "/static/Images/blazer.jpg", "size": "US 9", "type": "non-veg"},
    {"id": 6, "name": "Air Max 97", "brand": "NIKE", "price": "₹16,995", "price_raw": 16995, "image": "/static/Images/am97.jpg", "size": "US 11", "type": "veg"},
    {"id": 7, "name": "Jordan 4 'Military'", "brand": "JORDAN", "price": "₹24,500", "price_raw": 24500, "image": "/static/Images/military.jpg", "size": "US 10", "type": "non-veg"},
    {"id": 8, "name": "SB Dunk Low", "brand": "NIKE", "price": "₹11,500", "price_raw": 11500, "image": "/static/Images/sbdunk.jpg", "size": "US 9.5", "type": "non-veg"},

    # ADIDAS
    {"id": 9, "name": "Yeezy Slide 'Pure'", "brand": "ADIDAS", "price": "₹11,500", "price_raw": 11500, "image": "/static/Images/yeezy_slide.jpg", "size": "US 9", "type": "veg"},
    {"id": 10, "name": "Forum Low 'Vegan'", "brand": "ADIDAS", "price": "₹9,999", "price_raw": 9999, "image": "/static/Images/forum.jpg", "size": "US 11", "type": "veg"},
    {"id": 11, "name": "Superstar", "brand": "ADIDAS", "price": "₹7,999", "price_raw": 7999, "image": "/static/Images/superstar.jpg", "size": "US 8", "type": "non-veg"},

    # PUMA
    {"id": 17, "name": "RS-X Efekt", "brand": "PUMA", "price": "₹9,999", "price_raw": 9999, "image": "/static/Images/puma_rsx.jpg", "size": "US 10", "type": "veg"},
    {"id": 18, "name": "LaMelo Ball MB.02", "brand": "PUMA", "price": "₹14,999", "price_raw": 14999, "image": "/static/Images/mb02.jpg", "size": "US 11", "type": "veg"},
    {"id": 20, "name": "Mayze Stack", "brand": "PUMA", "price": "₹7,999", "price_raw": 7999, "image": "/static/Images/mayze.jpg", "size": "US 7", "type": "non-veg"}
]
# --- TEMPLATES ---
BASE_HEAD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SneakVault</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: { extend: { colors: { app: '#0B0B0B', card: '#181818', input: '#1F1F1F', accent: '#FF6B00' }, fontFamily: { sans: ['Inter', 'sans-serif'] } } }
        }
    </script>
    <style>body { background-color: #0B0B0B; color: white; } .hide-scrollbar::-webkit-scrollbar { display: none; }</style>
</head>
<body class="pb-24">
    <header class="sticky top-0 z-50 bg-app/95 backdrop-blur-md px-4 py-3 flex items-center justify-between border-b border-gray-800">
        <a href="/" class="flex items-center gap-2">
            <div class="bg-accent w-8 h-8 rounded-lg flex items-center justify-center"><i class="fa-solid fa-bolt text-white"></i></div>
            <h1 class="text-xl font-black tracking-tight">SNEAK<span class="font-light">VAULT</span></h1>
        </a>
        <div class="flex gap-5 items-center">
            <a href="/cart" class="relative">
                <i class="fa-solid fa-cart-shopping text-white text-lg hover:text-accent transition"></i>
                {% if cart_count > 0 %}
                <div class="absolute -top-2 -right-2 w-5 h-5 bg-accent rounded-full text-[10px] font-bold flex items-center justify-center border-2 border-app">
                    {{ cart_count }}
                </div>
                {% endif %}
            </a>
        </div>
    </header>
"""

HOME_TEMPLATE = BASE_HEAD + """
    <div class="px-4 mt-6">
        <div class="relative w-full h-64 rounded-2xl overflow-hidden bg-gradient-to-br from-[#1a1a1a] to-black border border-gray-800">
             <img src="/static/images/chicago.jpg" class="absolute right-[-20px] bottom-[-20px] w-64 object-cover transform rotate-[-15deg] drop-shadow-2xl opacity-90">
             <div class="absolute top-0 left-0 p-6 z-10 w-full h-full bg-gradient-to-r from-black/90 to-transparent">
                <span class="bg-accent text-white text-[10px] font-bold px-2 py-1 rounded mb-2 inline-block">TRENDING NOW</span>
                <h2 class="text-3xl font-bold leading-tight mb-2">Jordan 1 High<br>'Chicago'</h2>
                <p class="text-gray-400 text-xs mb-4">Last Sale: ₹64,000</p>
                <a href="/add/4" class="bg-white text-black text-xs font-bold px-4 py-2 rounded-lg hover:bg-gray-200">Buy Now</a>
             </div>
        </div>
    </div>

    <div class="px-4 mt-8 mb-4">
        <div class="flex bg-input rounded-lg p-1 gap-1">
            <button onclick="filter('veg')" id="btn-veg" class="flex-1 py-3 rounded font-bold text-xs uppercase bg-accent text-white shadow-lg flex items-center justify-center gap-2">
                <i class="fa-solid fa-leaf"></i> Veg (Vegan)
            </button>
            <button onclick="filter('non-veg')" id="btn-nonveg" class="flex-1 py-3 rounded font-bold text-xs uppercase text-gray-500 flex items-center justify-center gap-2">
                <i class="fa-solid fa-layer-group"></i> Non-Veg (Leather)
            </button>
        </div>
    </div>

    <section class="px-4">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-bold">Featured Drops</h3>
            <span class="text-xs text-accent animate-pulse">((●)) LIVE BIDS</span>
        </div>
        <div class="grid grid-cols-2 gap-4 pb-10">
            {% for p in products %}
            <div class="product-card bg-card rounded-xl p-3 group relative border border-gray-800" data-type="{{ p.type }}">
                <div class="bg-white rounded-lg h-32 w-full mb-3 flex items-center justify-center relative overflow-hidden">
                    <span class="absolute top-2 left-2 bg-black/80 text-white text-[10px] font-bold px-1.5 py-0.5 rounded">{{ p.size }}</span>
                    <img src="{{ p.image }}" class="w-full h-full object-contain p-2 mix-blend-multiply group-hover:scale-110 transition duration-300">
                </div>
                <p class="text-[10px] font-bold text-gray-500 uppercase">{{ p.brand }}</p>
                <h4 class="text-sm font-bold truncate">{{ p.name }}</h4>
                <div class="flex justify-between items-end mt-2">
                    <div>
                        <p class="text-[10px] text-gray-500">CURRENT BID</p>
                        <span class="text-lg font-bold">{{ p.price }}</span>
                    </div>
                    <a href="/add/{{ p.id }}" class="w-8 h-8 rounded-lg bg-accent flex items-center justify-center text-white hover:bg-orange-600 transition shadow-lg shadow-orange-900/20">
                        <i class="fa-solid fa-plus text-xs"></i>
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <script>
        function filter(type) {
            const cards = document.querySelectorAll('.product-card');
            const btnVeg = document.getElementById('btn-veg');
            const btnNon = document.getElementById('btn-nonveg');
            
            if(type === 'veg') {
                btnVeg.classList.add('bg-accent','text-white','shadow-lg'); btnVeg.classList.remove('text-gray-500');
                btnNon.classList.remove('bg-accent','text-white','shadow-lg'); btnNon.classList.add('text-gray-500');
            } else {
                btnNon.classList.add('bg-accent','text-white','shadow-lg'); btnNon.classList.remove('text-gray-500');
                btnVeg.classList.remove('bg-accent','text-white','shadow-lg'); btnVeg.classList.add('text-gray-500');
            }
            
            cards.forEach(card => {
                if(type === 'all') card.style.display = 'block';
                else card.style.display = (card.getAttribute('data-type') === type) ? 'block' : 'none';
            });
        }
        filter('veg'); // Default state
    </script>
</body>
</html>
"""

CART_TEMPLATE = BASE_HEAD + """
    <div class="px-4 py-6">
        <h2 class="text-2xl font-bold mb-6">Your Cart <span class="text-gray-500 text-sm font-normal">({{ cart_count }} items)</span></h2>
        
        {% if cart_count == 0 %}
            <div class="text-center py-20 opacity-50">
                <i class="fa-solid fa-basket-shopping text-6xl mb-4"></i>
                <p>Your cart is empty.</p>
                <a href="/" class="text-accent underline mt-2 inline-block">Start Shopping</a>
            </div>
        {% else %}
            <div class="space-y-4 pb-40">
                {% for item in items %}
                <div class="flex gap-4 bg-card p-3 rounded-xl border border-gray-800">
                    <div class="w-20 h-20 bg-white rounded-lg flex-shrink-0 flex items-center justify-center">
                         <img src="{{ item.image }}" class="w-16 mix-blend-multiply">
                    </div>
                    <div class="flex-1 flex flex-col justify-center">
                        <h4 class="font-bold text-sm">{{ item.name }}</h4>
                        <p class="text-xs text-gray-500">{{ item.brand }} | {{ item.size }}</p>
                        <div class="text-accent font-bold mt-1">{{ item.price }}</div>
                    </div>
                </div>
                {% endfor %}
            </div>

            <div class="fixed bottom-0 left-0 w-full bg-card border-t border-gray-800 p-6 rounded-t-3xl z-50">
                <div class="flex justify-between mb-2 text-gray-400 text-sm">
                    <span>Subtotal</span>
                    <span>₹{{ total }}</span>
                </div>
                <div class="flex justify-between mb-6 text-xl font-bold">
                    <span>Total</span>
                    <span>₹{{ total }}</span>
                </div>
                <div class="flex gap-3">
                    <a href="/clear_cart" class="flex-1 py-4 rounded-xl border border-gray-700 font-bold text-center hover:bg-gray-800">Clear</a>
                    <button onclick="alert('Proceeding to Payment Gateway...')" class="flex-[2] py-4 rounded-xl bg-accent font-bold text-white shadow-lg shadow-orange-900/20">Checkout</button>
                </div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_cart_details():
    cart_ids = session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        product = next((p for p in products if p['id'] == pid), None)
        if product:
            cart_items.append(product)
            total += product['price_raw']
    return cart_items, total

@app.route('/')
def home():
    cart = session.get('cart', [])
    return render_template_string(HOME_TEMPLATE, products=products, cart_count=len(cart))

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True 
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    cart_items, total_price = get_cart_details()
    return render_template_string(CART_TEMPLATE, items=cart_items, total=total_price, cart_count=len(cart_items))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    print("SneakVault Final is running on http://127.0.0.1:5000")

    app.run(debug=True)
