from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from extensions import db
from models.delivery import Delivery
from models.order import Order
from utils.security import role_required
import os
from werkzeug.utils import secure_filename

delivery_bp = Blueprint("delivery", __name__, url_prefix="/delivery")

def _save_proof_image(file_storage):
    if not file_storage or file_storage.filename == "":
        return None

    upload_root = os.path.join(current_app.static_folder, "uploads", "proofs")
    os.makedirs(upload_root, exist_ok=True)
    
    filename = secure_filename(file_storage.filename)
    path = os.path.join(upload_root, filename)
    
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(path):
        filename = f"{base}_{counter}{ext}"
        path = os.path.join(upload_root, filename)
        counter += 1

    file_storage.save(path)
    return f"/static/uploads/proofs/{filename}"

@delivery_bp.route("/home")
@login_required
@role_required("DELIVERY")
def home():
    # Calculate total earnings (simplified - assuming fixed delivery fee)
    completed_deliveries_count = Delivery.query.filter_by(
        delivery_partner_id=current_user.id,
        status="DELIVERED"
    ).count()
    total_earnings = completed_deliveries_count * 50  # Assuming ₹50 per delivery
    
    # Active deliveries
    active_deliveries = Delivery.query.filter_by(
        delivery_partner_id=current_user.id
    ).filter(
        Delivery.status.in_(["ASSIGNED", "ACCEPTED", "PICKED_UP", "ON_THE_WAY"])
    ).count()
    
    # Success rate
    total_deliveries = Delivery.query.filter_by(delivery_partner_id=current_user.id).count()
    success_rate = int((completed_deliveries_count / total_deliveries * 100)) if total_deliveries > 0 else 100
    
    # Active deliveries list
    active_deliveries_list = (
        Delivery.query.filter_by(delivery_partner_id=current_user.id)
        .filter(Delivery.status.in_(["ASSIGNED", "ACCEPTED", "PICKED_UP", "ON_THE_WAY"]))
        .order_by(Delivery.updated_at.desc())
        .limit(4)
        .all()
    )
    
    # Recent earnings (completed deliveries)
    recent_earnings = (
        Delivery.query.filter_by(delivery_partner_id=current_user.id, status="DELIVERED")
        .order_by(Delivery.updated_at.desc())
        .limit(5)
        .all()
    )
    
    return render_template(
        "delivery/home.html",
        total_earnings=total_earnings,
        active_deliveries=active_deliveries,
        completed_deliveries=completed_deliveries_count,
        success_rate=success_rate,
        active_deliveries_list=active_deliveries_list,
        recent_earnings=recent_earnings
    )

@delivery_bp.route("/dashboard")
@login_required
@role_required("DELIVERY")
def dashboard():
    # Get deliveries assigned to this partner
    deliveries = (
        Delivery.query.filter_by(delivery_partner_id=current_user.id)
        .order_by(Delivery.updated_at.desc())
        .all()
    )
    return render_template("delivery/dashboard.html", deliveries=deliveries)

@delivery_bp.route("/update-status/<int:delivery_id>", methods=["POST"])
@login_required
@role_required("DELIVERY")
def update_status(delivery_id):
    delivery = Delivery.query.filter_by(id=delivery_id, delivery_partner_id=current_user.id).first_or_404()
    
    new_status = request.form.get("status")
    if new_status not in ["ACCEPTED", "PICKED_UP", "ON_THE_WAY", "DELIVERED"]:
        flash("Invalid status", "error")
        return redirect(url_for("delivery.dashboard"))
        
    delivery.status = new_status
    
    # Sync order status
    if new_status == "DELIVERED":
        delivery.order.status = "DELIVERED"
        
        # Handle proof upload
        proof_image = request.files.get("proof_image")
        if proof_image:
            image_url = _save_proof_image(proof_image)
            delivery.proof_image_url = image_url
            
            # Blockchain Integration
            from services.blockchain_service import blockchain_service
            from models.blockchain_order import BlockchainOrder
            
            # Generate hash of the proof
            proof_data = f"{delivery.id}-{image_url}-{delivery.updated_at}"
            proof_hash = blockchain_service.generate_hash(proof_data)
            delivery.proof_hash_on_chain = proof_hash
            
            # Submit delivery proof to blockchain
            tx_hash_proof = blockchain_service.submit_delivery_proof(
                delivery.order.id,
                proof_hash
            )
            
            if tx_hash_proof:
                print(f"[INFO] Delivery proof submitted to blockchain: {tx_hash_proof}")
                
                # Release funds from escrow to farmer
                tx_hash_release = blockchain_service.release_funds(delivery.order.id)
                
                if tx_hash_release:
                    # Update blockchain order state
                    blockchain_order = BlockchainOrder.query.filter_by(order_id=delivery.order.id).first()
                    if blockchain_order:
                        blockchain_order.state = "FUNDS_RELEASED"
                        blockchain_order.tx_hash_release = tx_hash_release
                        db.session.commit()
                    
                    print(f"[INFO] Funds released to farmer: {tx_hash_release}")
                    flash("Delivery completed and funds released to farmer!", "success")
                else:
                    flash("Delivery marked, but fund release pending.", "warning")
            else:
                flash("Delivery marked, but blockchain proof submission pending.", "warning")
        else:
            flash("Please upload proof of delivery", "error")
            return redirect(url_for("delivery.dashboard"))

    elif new_status == "ON_THE_WAY":
        delivery.order.status = "OUT_FOR_DELIVERY"
        
    db.session.commit()
    flash(f"Status updated to {new_status}", "success")
    return redirect(url_for("delivery.dashboard"))

# Additional routes for delivery home page

@delivery_bp.route("/available-deliveries")
@login_required
@role_required("DELIVERY")
def available_deliveries():
    # Show unassigned deliveries
    available = Order.query.filter(
        Order.status.in_(["FARMER_CONFIRMED", "PAID"]),
        Order.delivery_partner_id == None
    ).order_by(Order.created_at.desc()).all()
    
    return render_template("delivery/available_deliveries.html", orders=available)

@delivery_bp.route("/my-deliveries")
@login_required
@role_required("DELIVERY")
def my_deliveries():
    deliveries = (
        Delivery.query.filter_by(delivery_partner_id=current_user.id)
        .order_by(Delivery.updated_at.desc())
        .all()
    )
    return render_template("delivery/my_deliveries.html", deliveries=deliveries)

@delivery_bp.route("/earnings")
@login_required
@role_required("DELIVERY")
def earnings():
    completed = (
        Delivery.query.filter_by(delivery_partner_id=current_user.id, status="DELIVERED")
        .order_by(Delivery.updated_at.desc())
        .all()
    )
    total_earnings = len(completed) * 50  # Assuming ₹50 per delivery
    return render_template("delivery/earnings.html", deliveries=completed, total_earnings=total_earnings)

@delivery_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("DELIVERY")
def profile():
    if request.method == "POST":
        # Update profile
        current_user.name = request.form.get("name", current_user.name)
        current_user.phone = request.form.get("phone", current_user.phone)
        current_user.address = request.form.get("address", current_user.address)
        
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("delivery.profile"))
    
    return render_template("delivery/profile.html")

@delivery_bp.route("/delivery/<int:delivery_id>")
@login_required
@role_required("DELIVERY")
def delivery_detail(delivery_id):
    delivery = Delivery.query.filter_by(
        id=delivery_id,
        delivery_partner_id=current_user.id
    ).first_or_404()
    return render_template("delivery/delivery_detail.html", delivery=delivery)
