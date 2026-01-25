
from flask import Flask, render_template_string, request, jsonify, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-in-production"  # TODO: move to env var

# Sample products with free images from Picsum
products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "price": 99.99,
        "image": "https://picsum.photos/300/200?random=1",
        "category": "Electronics",
        "description": "High-quality wireless headphones with noise cancellation",
        "rating": 4.5,
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "price": 199.99,
        "image": "https://picsum.photos/300/200?random=2",
        "category": "Electronics",
        "description": "Feature-rich smartwatch with health monitoring",
        "rating": 4.2,
    },
    {
        "id": 3,
        "name": "Running Shoes",
        "price": 79.99,
        "image": "https://picsum.photos/300/200?random=3",
        "category": "Fashion",
        "description": "Comfortable running shoes for all terrains",
        "rating": 4.7,
    },
    {
        "id": 4,
        "name": "Coffee Maker",
        "price": 49.99,
        "image": "https://picsum.photos/300/200?random=4",
        "category": "Home",
        "description": "Automatic coffee maker with timer",
        "rating": 4.3,
    },
    {
        "id": 5,
        "name": "Backpack",
        "price": 39.99,
        "image": "https://picsum.photos/300/200?random=5",
        "category": "Fashion",
        "description": "Waterproof backpack with laptop compartment",
        "rating": 4.6,
    },
    {
        "id": 6,
        "name": "Desk Lamp",
        "price": 29.99,
        "image": "https://picsum.photos/300/200?random=6",
        "category": "Home",
        "description": "LED desk lamp with adjustable brightness",
        "rating": 4.4,
    },
]

# HTML Template for E‑commerce App
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>ShopEasy - Online Store</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet"/>
  <style>
    :root { --brand:#2563eb; --muted:#64748b; --bg:#0b1020; --card:#0f172a; --text:#e2e8f0; }
    *{ box-sizing:border-box; }
    body{ margin:0; font-family:Inter,system-ui,Segoe UI,Arial; background:linear-gradient(180deg,#0b1020,#0a0f1f 30%,#0f172a); color:var(--text); }
    header{ padding:24px 16px; border-bottom:1px solid #1f2937; background:rgba(2,6,23,.6); backdrop-filter:saturate(140%) blur(6px); position:sticky; top:0; }
    .container{ max-width:1100px; margin:0 auto; }
    .title{ display:flex; align-items:center; gap:10px; font-weight:700; }
    .grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px; margin:20px 0 28px; }
    .card{ background:linear-gradient(180deg,#0f172a,#0b1226); border:1px solid #1f2937; border-radius:12px; overflow:hidden; box-shadow:0 12px 30px rgba(0,0,0,.35); }
    .card img{ width:100%; height:150px; object-fit:cover; display:block; }
    .pad{ padding:14px; }
    .name{ font-weight:600; margin:0 0 6px; }
    .desc{ color:var(--muted); font-size:.95rem; min-height:42px; }
    .price{ font-weight:700; margin-top:10px; }
    .button{ background:var(--brand); color:#fff; border:0; padding:10px 12px; border-radius:8px; cursor:pointer; margin-top:12px; width:100%; }
    .chips{ display:flex; gap:8px; margin:14px 0; flex-wrap:wrap; }
    .chip{ background:#0b1224; color:#cbd5e1; border:1px solid #1f2937; padding:6px 10px; border-radius:999px; cursor:pointer; }
    .row{ display:flex; gap:20px; align-items:flex-start; }
    .cart{ background:linear-gradient(180deg,#0f172a,#0b1226); border:1px solid #1f2937; border-radius:12px; padding:16px; width:320px; position:sticky; top:84px; height:fit-content; }
    .cart h3{ margin:0 0 8px; }
    .cart-item{ display:flex; gap:10px; align-items:center; justify-content:space-between; padding:8px 0; border-bottom:1px dashed #1f2937; }
    .qty{ display:flex; gap:6px; align-items:center; }
    .qty input{ width:56px; background:#0b1224; border:1px solid #1f2937; color:#e2e8f0; border-radius:6px; padding:4px 6px; }
    footer{ color:#9ca3af; padding:22px 0 40px; text-align:center; border-top:1px solid #1f2937; }
    @media (max-width:960px){ .row{ flex-direction:column; } .cart{ width:auto; position:relative; top:0; } }
  </style>
</head>
<body>
  <header>
    <div class="container title">
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M3 6h18l-2 12H5L3 6Z" stroke="#60a5fa" stroke-width="1.5"/><circle cx="9" cy="20" r="1" fill="#93c5fd"/><circle cx="17" cy="20" r="1" fill="#93c5fd"/></svg>
      <div>ShopEasy</div>
    </div>
  </header>

  <div class="container">
    <h2 style="margin:22px 0 8px;">Welcome to ShopEasy</h2>
    <div style="color:#9ca3af;margin-bottom:18px;">Discover amazing products at great prices</div>

    <div class="row">
      <main style="flex:1">
        <div class="chips">
          <div class="chip" onclick="filterCategory('All')">All</div>
          <div class="chip" onclick="filterCategory('Electronics')">Electronics</div>
          <div class="chip" onclick="filterCategory('Fashion')">Fashion</div>
          <div class="chip" onclick="filterCategory('Home')">Home</div>
        </div>

        <div id="grid" class="grid">
          {% for product in products %}
          <div class="card" data-category="{{ product.category }}">
            <img src="{{ product.image }}" alt="{{ product.name }}"/>
            <div class="pad">
              <p class="name">{{ product.name }}</p>
              <p class="desc">{{ product.description }}</p>
              <div class="price">${{ "%.2f"|format(product.price) }}</div>
              <button class="button" onclick="addToCart({{ product.id }})">Add to Cart</button>
            </div>
          </div>
          {% endfor %}
        </div>
      </main>

      <aside class="cart">
        <h3>Your Shopping Cart</h3>
        <div id="cart-empty">Your cart is empty</div>
        <div id="cart-items"></div>
        <div style="display:flex;justify-content:space-between;margin-top:10px;">
          <strong>Total: $<span id="cart-total">0.00</span></strong>
          <button class="button" style="width:auto" onclick="checkout()">Checkout</button>
        </div>
      </aside>
    </div>
  </div>

  <footer>
    © {{ now }} ShopEasy. All rights reserved. Built with ❤️ using Flask.
  </footer>

<script>
async function addToCart(productId){
  const r = await fetch('/add_to_cart',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({product_id:productId})});
  const data = await r.json();
  renderCart(data.cart || []);
}
async function removeFromCart(productId){
  const r = await fetch('/remove_from_cart',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({product_id:productId})});
  const data = await r.json();
  renderCart(data.cart || []);
}
async function updateQty(productId, qty){
  const q = parseInt(qty,10) || 0;
  const r = await fetch('/update_quantity',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({product_id:productId, quantity:q})});
  const data = await r.json();
  renderCart(data.cart || []);
}
async function checkout(){
  const r = await fetch('/checkout',{method:'POST'});
  const data = await r.json();
  alert(data.message || 'Done');
  renderCart([]);
}

function renderCart(cart){
  const items = document.getElementById('cart-items');
  const empty = document.getElementById('cart-empty');
  const total = document.getElementById('cart-total');

  if(!cart || cart.length === 0){
    items.innerHTML = '';
    empty.style.display = 'block';
    total.textContent = '0.00';
    return;
  }
  empty.style.display = 'none';
  let sum = 0;
  items.innerHTML = cart.map(item=>{
    const line = item.price * item.quantity;
    sum += line;
    return `
      <div class="cart-item">
        <div style="flex:1 1 auto;">
          <div style="font-weight:600;">${item.name}</div>
          <div style="color:#9ca3af;">$${item.price.toFixed(2)}</div>
        </div>
        <div class="qty">
          <input type="number" min="0" value="${item.quantity}" onchange="updateQty(${item.id}, this.value)"/>
          <button class="button" style="width:auto" onclick="removeFromCart(${item.id})">Remove</button>
        </div>
      </div>`;
  }).join('');
  total.textContent = sum.toFixed(2);
}

function filterCategory(cat){
  const cards = document.querySelectorAll('#grid .card');
  cards.forEach(c=>{
    const match = (cat === 'All') || (c.getAttribute('data-category') === cat);
    c.style.display = match ? 'block' : 'none';
  });
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, products=products, now=datetime.utcnow().year)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if "cart" not in session:
        session["cart"] = []
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")

    # Find the product
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        cart = session["cart"]
        cart_item = next((item for item in cart if item["id"] == product_id), None)
        if cart_item:
            cart_item["quantity"] += 1
        else:
            cart.append(
                {
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "image": product["image"],
                    "quantity": 1,
                }
            )
        session["cart"] = cart
        return jsonify({"success": True, "cart": cart})
    return jsonify({"success": False}), 400

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    if "cart" in session:
        session["cart"] = [item for item in session["cart"] if item["id"] != product_id]
        return jsonify({"success": True, "cart": session["cart"]})
    return jsonify({"success": False}), 400

@app.route("/update_quantity", methods=["POST"])
def update_quantity():
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = int(data.get("quantity") or 0)

    if "cart" in session:
        cart = session["cart"]
        cart_item = next((item for item in cart if item["id"] == product_id), None)
        if cart_item:
            if quantity <= 0:
                session["cart"] = [item for item in cart if item["id"] != product_id]
            else:
                cart_item["quantity"] = quantity
            return jsonify({"success": True, "cart": session["cart"]})
    return jsonify({"success": False}), 400

@app.route("/get_cart")
def get_cart():
    return jsonify(session.get("cart", []))

@app.route("/checkout", methods=["POST"])
def checkout():
    if "cart" in session and session["cart"]:
        # In a real app, you'd process payment and save order
        session["cart"] = []
        return jsonify({"success": True, "message": "Order placed successfully!"})
    return jsonify({"success": False, "message": "Cart is empty!"}), 400

if __name__ == "__main__":
    # IMPORTANT: Bind to 0.0.0.0 so it works in Kubernetes
    app.run(host="0.0.0.0", port=5000, debug=False)
