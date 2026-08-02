from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from extensions import db
from models.product import Product
from models.cart import Cart, CartItem
from models.order import Order, OrderItem
from utils.security import role_required

buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")

@buyer_bp.route("/home")
@login_required
@role_required("BUYER")
def home():
    # Fetch statistics
    total_orders = Order.query.filter_by(buyer_id=current_user.id).count()
    pending_orders = Order.query.filter_by(buyer_id=current_user.id).filter(
        Order.status.in_(["PENDING_PAYMENT", "CONFIRMED", "OUT_FOR_DELIVERY"])
    ).count()
    delivered_orders = Order.query.filter_by(buyer_id=current_user.id, status="DELIVERED").count()
    
    # Calculate total spent
    total_spent = db.session.query(db.func.sum(Order.total_amount)).filter_by(
        buyer_id=current_user.id
    ).scalar() or 0
    
    # Recent orders (last 5)
    recent_orders = (
        Order.query.filter_by(buyer_id=current_user.id)
        .order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )
    
    # Featured products (approved products, random selection)
    featured_products = (
        Product.query.filter_by(status="APPROVED")
        .order_by(db.func.random())
        .limit(8)
        .all()
    )
    
    return render_template(
        "buyer/home.html",
        total_orders=total_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        total_spent=total_spent,
        recent_orders=recent_orders,
        featured_products=featured_products
    )

@buyer_bp.route("/dashboard")
@login_required
@role_required("BUYER")
def dashboard():
    # Recent orders
    recent_orders = (
        Order.query.filter_by(buyer_id=current_user.id)
        .order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )
    return render_template("buyer/dashboard.html", recent_orders=recent_orders)

@buyer_bp.route("/shop")
def shop():
    # Show all APPROVED products
    products = Product.query.filter_by(status="APPROVED").all()
    return render_template("buyer/shop.html", products=products)

@buyer_bp.route("/cart")
@login_required
@role_required("BUYER")
def cart_view():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart_items = []
        total = 0
    else:
        cart_items = cart.items
        total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template("buyer/cart.html", cart=cart, cart_items=cart_items, total=total)

@buyer_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
@role_required("BUYER")
def add_to_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    
    # Get product to fetch price
    product = Product.query.get_or_404(product_id)
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    # Check if item exists
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart.id, 
            product_id=product_id, 
            quantity=quantity,
            unit_price=product.price  # Add unit_price from product
        )
        db.session.add(item)
    
    db.session.commit()
    flash("Added to cart", "success")
    return redirect(url_for("buyer.shop"))

@buyer_bp.route("/cart/remove/<int:item_id>", methods=["POST"])
@login_required
@role_required("BUYER")
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.cart.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for("buyer.cart_view"))
        
    db.session.delete(item)
    db.session.commit()
    flash("Removed from cart", "success")
    return redirect(url_for("buyer.cart_view"))

@buyer_bp.route("/checkout", methods=["GET", "POST"])
@login_required
@role_required("BUYER")
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash("Cart is empty", "warning")
        return redirect(url_for("buyer.shop"))
        
    if request.method == "POST":
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        city = request.form.get("city")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        payment_method = request.form.get("payment", "COD")
        
        if not address or not pincode or not city:
            flash("Please fill all address fields", "error")
            return redirect(url_for("buyer.checkout"))
        
        if not latitude or not longitude:
            flash("Please select delivery location on map", "error")
            return redirect(url_for("buyer.checkout"))
            
        # Group items by farmer to create separate orders
        items_by_farmer = {}
        for item in cart.items:
            fid = item.product.farmer_id
            if fid not in items_by_farmer:
                items_by_farmer[fid] = []
            items_by_farmer[fid].append(item)
            
        import uuid
        
        for fid, items in items_by_farmer.items():
            total_amount = sum(i.product.price * i.quantity for i in items)
            
            # Create full address string with location
            full_address = f"{address}, {city} - {pincode}\nLocation: {latitude}, {longitude}"
            
            order = Order(
                order_uuid=str(uuid.uuid4()),
                buyer_id=current_user.id,
                farmer_id=fid,
                total_amount=total_amount,
                delivery_address=full_address,
                status="PENDING_PAYMENT"
            )
            db.session.add(order)
            db.session.flush()
            
            for item in items:
                oi = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.product.price
                )
                db.session.add(oi)
                
        # Clear cart
        for item in cart.items:
            db.session.delete(item)
        db.session.commit()
        
        # If online payment, redirect to payment page
        if payment_method == "ONLINE":
            # Get the last created order for payment
            last_order = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_at.desc()).first()
            return redirect(url_for("payment.create_order", order_id=last_order.id))
        else:
            flash("Order placed successfully! Waiting for farmer confirmation.", "success")
            return redirect(url_for("buyer.dashboard"))
    
    return render_template("buyer/checkout.html", cart=cart)


@buyer_bp.route("/order/<int:order_id>")
@login_required
@role_required("BUYER")
def order_detail(order_id):
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first_or_404()
    return render_template("buyer/order_detail.html", order=order)

@buyer_bp.route("/orders")
@login_required
@role_required("BUYER")
def orders():
    all_orders = (
        Order.query.filter_by(buyer_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("buyer/orders.html", orders=all_orders)

@buyer_bp.route("/addresses")
@login_required
@role_required("BUYER")
def addresses():
    # For now, render a simple addresses page
    # You can expand this later with a proper Address model
    return render_template("buyer/addresses.html")

@buyer_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("BUYER")
def profile():
    if request.method == "POST":
        # Update profile
        current_user.name = request.form.get("name", current_user.name)
        current_user.phone = request.form.get("phone", current_user.phone)
        current_user.address = request.form.get("address", current_user.address)
        
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("buyer.profile"))
    
    return render_template("buyer/profile.html")
