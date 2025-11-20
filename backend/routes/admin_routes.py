# backend/routes/admin_routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from extensions import db
from models.user import User
from models.product import Product
from models.order import Order
from models.delivery import Delivery
from utils.security import login_required, role_required

admin_bp = Blueprint("admin", __name__)

# ---------- DASHBOARD ----------

@admin_bp.route("/dashboard")
@login_required
@role_required("ADMIN")
def dashboard():
    # High-level stats
    total_users = User.query.count()
    farmers_count = User.query.filter_by(role="FARMER").count()
    buyers_count = User.query.filter_by(role="BUYER").count()
    delivery_count = User.query.filter_by(role="DELIVERY").count()

    total_orders = Order.query.count()

    pending_users = User.query.filter_by(is_approved=False).all()
    pending_products = Product.query.filter_by(status="PENDING_APPROVAL").all()

    pending_users_count = len(pending_users)
    pending_products_count = len(pending_products)

    recent_orders = (
        Order.query.order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        farmers_count=farmers_count,
        buyers_count=buyers_count,
        delivery_count=delivery_count,
        total_orders=total_orders,
        pending_users_count=pending_users_count,
        pending_products_count=pending_products_count,
        pending_users=pending_users,
        pending_products=pending_products,
        recent_orders=recent_orders,
    )


# ---------- USER APPROVALS ----------

@admin_bp.route("/users")
@login_required
@role_required("ADMIN")
def users_list():
    """List all users with focus on pending approvals."""
    pending_users = User.query.filter_by(is_approved=False).all()
    approved_users = User.query.filter_by(is_approved=True).all()

    return render_template(
        "admin/users.html",
        pending_users=pending_users,
        approved_users=approved_users,
    )


@admin_bp.route("/users/<int:user_id>/approve", methods=["POST"])
@login_required
@role_required("ADMIN")
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    user.is_active = True
    db.session.commit()
    flash(f"User {user.name} approved.", "success")
    return redirect(request.referrer or url_for("admin.dashboard"))


@admin_bp.route("/users/<int:user_id>/deactivate", methods=["POST"])
@login_required
@role_required("ADMIN")
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    flash(f"User {user.name} deactivated.", "warning")
    return redirect(request.referrer or url_for("admin.dashboard"))


# ---------- PRODUCT APPROVALS ----------

@admin_bp.route("/products")
@login_required
@role_required("ADMIN")
def products_list():
    pending_products = Product.query.filter_by(status="PENDING_APPROVAL").all()
    approved_products = Product.query.filter_by(status="APPROVED").all()
    rejected_products = Product.query.filter_by(status="REJECTED").all()

    return render_template(
        "admin/products.html",
        pending_products=pending_products,
        approved_products=approved_products,
        rejected_products=rejected_products,
    )


@admin_bp.route("/products/<int:product_id>/approve", methods=["POST"])
@login_required
@role_required("ADMIN")
def approve_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.status = "APPROVED"
    db.session.commit()
    flash(f"Product '{product.name}' approved.", "success")
    return redirect(request.referrer or url_for("admin.dashboard"))


@admin_bp.route("/products/<int:product_id>/reject", methods=["POST"])
@login_required
@role_required("ADMIN")
def reject_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.status = "REJECTED"
    db.session.commit()
    flash(f"Product '{product.name}' rejected.", "danger")
    return redirect(request.referrer or url_for("admin.dashboard"))


@admin_bp.route("/deliveries")
@role_required("ADMIN")
def deliveries():
    # Get orders that need delivery partner assignment
    # Include PENDING_PAYMENT (COD), PAID (online payment completed), and FARMER_CONFIRMED
    # Exclude orders that already have delivery assigned
    pending_delivery_orders = Order.query.filter(
        Order.status.in_(["PENDING_PAYMENT", "PAID", "FARMER_CONFIRMED"]),
        Order.delivery_partner_id == None
    ).order_by(Order.created_at.desc()).all()

    delivery_partners = User.query.filter_by(role="DELIVERY", is_approved=True).all()

    active_deliveries = Delivery.query.filter(
        Delivery.status.in_(["ASSIGNED", "ACCEPTED", "PICKED_UP", "ON_THE_WAY"])
    ).order_by(Delivery.updated_at.desc()).all()

    return render_template(
        "admin/deliveries.html",
        pending_delivery_orders=pending_delivery_orders,
        delivery_partners=delivery_partners,
        active_deliveries=active_deliveries
    )



@admin_bp.route("/assign-delivery/<int:order_id>", methods=["POST"])
@role_required("ADMIN")
def assign_delivery_partner(order_id):
    delivery_partner_id = request.form.get("delivery_partner_id")
    
    if not delivery_partner_id:
        flash("Please select a delivery partner", "error")
        return redirect(url_for("admin.deliveries"))

    # Create delivery record
    delivery = Delivery(
        order_id=order_id,
        delivery_partner_id=delivery_partner_id,
        status="ASSIGNED"
    )
    db.session.add(delivery)

    # Update order status and assign delivery partner
    order = Order.query.get(order_id)
    order.status = "ASSIGNED_DELIVERY"
    order.delivery_partner_id = delivery_partner_id

    db.session.commit()

    flash("Delivery partner assigned successfully!", "success")
    return redirect(url_for("admin.deliveries"))
