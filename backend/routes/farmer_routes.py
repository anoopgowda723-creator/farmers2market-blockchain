from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from flask_login import current_user
import os
from werkzeug.utils import secure_filename

from extensions import db
from utils.security import login_required, role_required
from models.user import User
from models.product import Product
from models.order import Order
# from models.delivery import Delivery   # we’ll plug this in later

farmer_bp = Blueprint("farmer", __name__, url_prefix="/farmer")


# ---------- Helpers ----------

def _ensure_upload_folder():
    upload_root = os.path.join(current_app.static_folder, "uploads", "products")
    os.makedirs(upload_root, exist_ok=True)
    return upload_root


def _save_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None

    upload_root = _ensure_upload_folder()
    filename = secure_filename(file_storage.filename)
    path = os.path.join(upload_root, filename)

    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(path):
        filename = f"{base}_{counter}{ext}"
        path = os.path.join(upload_root, filename)
        counter += 1

    file_storage.save(path)
    return f"/static/uploads/products/{filename}"


# ---------- Dashboard ----------

@farmer_bp.route("/dashboard")
@login_required
@role_required("FARMER")
def dashboard():
    # use getattr so it doesn't crash if columns/attrs don't exist yet
    payout_missing = not (
        getattr(current_user, "bank_account_no", None)
        and getattr(current_user, "ifsc_code", None)
        and (
            getattr(current_user, "upi_id", None)
            or getattr(current_user, "wallet_address", None)
        )
    )

    location_missing = not (
        getattr(current_user, "address", None)
        and getattr(current_user, "warehouse_lat", None)
        and getattr(current_user, "warehouse_lng", None)
    )

    products_query = (
        Product.query
        .filter_by(farmer_id=current_user.id)
        .order_by(Product.created_at.desc())
    )
    products = products_query.all()

    total_products = len(products)
    pending_count = sum(1 for p in products if p.status == "PENDING_APPROVAL")
    live_count = sum(1 for p in products if p.status == "APPROVED")
    rejected_count = sum(1 for p in products if p.status == "REJECTED")
    out_of_stock_count = sum(
        1 for p in products
        if p.stock is not None and p.stock <= 0
    )

    approved_products = live_count
    pending_products = pending_count
    rejected_products = rejected_count

    open_orders_count = (
        Order.query.filter(
            Order.farmer_id == current_user.id,
            Order.status.in_(["PAID", "FARMER_CONFIRMED"]),
        ).count()
    )

    latest_products = products[:5]

    recent_orders = (
        Order.query.filter_by(farmer_id=current_user.id)
        .order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "farmer/dashboard.html",
        products=products,
        latest_products=latest_products,
        recent_orders=recent_orders,
        total_products=total_products,
        approved_products=approved_products,
        pending_products=pending_products,
        rejected_products=rejected_products,
        pending_count=pending_count,
        live_count=live_count,
        out_of_stock_count=out_of_stock_count,
        open_orders_count=open_orders_count,
        payout_missing=payout_missing,
        location_missing=location_missing,
    )


# ---------- Profile / Payment + Location ----------

@farmer_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("FARMER")
def profile():
    user = current_user

    if request.method == "POST":
        user.name = request.form.get("name", user.name)
        user.phone = request.form.get("phone", user.phone)
        user.address = request.form.get("address", getattr(user, "address", None))

        # Only set these if the model actually has the attributes
        if hasattr(user, "bank_account_no"):
            user.bank_account_no = request.form.get("bank_account_no") or None
        if hasattr(user, "ifsc_code"):
            user.ifsc_code = request.form.get("ifsc_code") or None
        if hasattr(user, "upi_id"):
            user.upi_id = request.form.get("upi_id") or None
        if hasattr(user, "wallet_address"):
            user.wallet_address = request.form.get("wallet_address") or None

        if hasattr(user, "warehouse_lat"):
            lat_val = request.form.get("warehouse_lat")
            if lat_val:
                try:
                    user.warehouse_lat = float(lat_val)
                except ValueError:
                    pass

        if hasattr(user, "warehouse_lng"):
            lng_val = request.form.get("warehouse_lng")
            if lng_val:
                try:
                    user.warehouse_lng = float(lng_val)
                except ValueError:
                    pass

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("farmer.profile"))

    return render_template("farmer/profile.html", user=user)


# ---------- Products ----------

@farmer_bp.route("/products")
@login_required
@role_required("FARMER")
def products_list():
    products = (
        Product.query.filter_by(farmer_id=current_user.id)
        .order_by(Product.created_at.desc())
        .all()
    )
    return render_template("farmer/products.html", products=products)


@farmer_bp.route("/products/new", methods=["GET", "POST"])
@login_required
@role_required("FARMER")
def product_create():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        unit_label = request.form.get("unit_label") or "kg"

        if not name or not price or not stock:
            flash("Name, price and stock are required.", "error")
            return redirect(url_for("farmer.product_create"))

        try:
            price_val = float(price)
            stock_val = int(stock)
        except ValueError:
            flash("Price must be a number and stock must be an integer.", "error")
            return redirect(url_for("farmer.product_create"))

        image1_url = _save_image(request.files.get("image1"))
        image2_url = _save_image(request.files.get("image2"))
        image3_url = _save_image(request.files.get("image3"))

        product = Product(
            farmer_id=current_user.id,
            name=name,
            description=description,
            price=price_val,
            stock=stock_val,
            image1_url=image1_url,
            image2_url=image2_url,
            image3_url=image3_url,
            status="PENDING_APPROVAL",
        )

        if hasattr(Product, "unit_label"):
            product.unit_label = unit_label

        db.session.add(product)
        db.session.commit()

        flash("Product submitted for approval.", "success")
        return redirect(url_for("farmer.products_list"))

    return render_template(
        "farmer/product_form.html",
        product=None,
        is_edit=False,
    )


@farmer_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("FARMER")
def product_edit(product_id):
    product = (
        Product.query.filter_by(id=product_id, farmer_id=current_user.id)
        .first_or_404()
    )

    if request.method == "POST":
        product.name = request.form.get("name") or product.name
        product.description = request.form.get("description") or product.description

        price = request.form.get("price")
        stock = request.form.get("stock")
        unit_label = request.form.get("unit_label")

        if price:
            try:
                product.price = float(price)
            except ValueError:
                flash("Invalid price.", "error")
                return redirect(url_for("farmer.product_edit", product_id=product.id))

        if stock:
            try:
                product.stock = int(stock)
            except ValueError:
                flash("Invalid stock.", "error")
                return redirect(url_for("farmer.product_edit", product_id=product.id))

        if unit_label and hasattr(Product, "unit_label"):
            product.unit_label = unit_label

        new_img1 = _save_image(request.files.get("image1"))
        new_img2 = _save_image(request.files.get("image2"))
        new_img3 = _save_image(request.files.get("image3"))
        if new_img1:
            product.image1_url = new_img1
        if new_img2:
            product.image2_url = new_img2
        if new_img3:
            product.image3_url = new_img3

        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("farmer.products_list"))

    return render_template(
        "farmer/product_form.html",
        product=product,
        is_edit=True,
    )


# ---------- Orders for Farmer ----------

@farmer_bp.route("/orders")
@login_required
@role_required("FARMER")
def orders_list():
    tab = request.args.get("tab", "open")

    base_query = Order.query.filter_by(farmer_id=current_user.id)

    if tab == "completed":
        orders = (
            base_query
            .filter(Order.status.in_(["DELIVERED", "COMPLETED", "REFUNDED"]))
            .order_by(Order.created_at.desc())
            .all()
        )
    elif tab == "all":
        orders = base_query.order_by(Order.created_at.desc()).all()
    else:  # "open"
        orders = (
            base_query
            .filter(
                Order.status.in_(
                    ["PAID", "FARMER_CONFIRMED", "ASSIGNED_DELIVERY", "OUT_FOR_DELIVERY"]
                )
            )
            .order_by(Order.created_at.desc())
            .all()
        )

    return render_template("farmer/orders.html", orders=orders, active_tab=tab)


@farmer_bp.route("/orders/<int:order_id>")
@login_required
@role_required("FARMER")
def order_detail(order_id):
    order = (
        Order.query.filter_by(id=order_id, farmer_id=current_user.id)
        .first_or_404()
    )
    return render_template("farmer/order_detail.html", order=order)


@farmer_bp.route("/orders/<int:order_id>/confirm", methods=["POST"])
@login_required
@role_required("FARMER")
def order_confirm(order_id):
    order = Order.query.get_or_404(order_id)
    if order.farmer_id != current_user.id:
        flash("Unauthorized", "error")
        return redirect(url_for("farmer.dashboard"))
    
    if order.status == "PAID":
        order.status = "FARMER_CONFIRMED"
        db.session.commit()
        
        # Update blockchain state
        from services.blockchain_service import blockchain_service
        from models.blockchain_order import BlockchainOrder
        
        blockchain_order = BlockchainOrder.query.filter_by(order_id=order.id).first()
        if blockchain_order:
            tx_hash = blockchain_service.mark_farmer_confirmed(order.id)
            if tx_hash:
                blockchain_order.state = "FARMER_CONFIRMED"
                # You could store this tx_hash in a new field if needed
                db.session.commit()
                print(f"[INFO] Farmer confirmed order {order.id} on blockchain: {tx_hash}")
        
        flash("Order confirmed!", "success")
    
    return redirect(url_for("farmer.orders_list", tab="open"))
