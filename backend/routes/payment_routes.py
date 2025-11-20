from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.order import Order
from models.payment import Payment
from models.blockchain_order import BlockchainOrder
from services.payment_service import payment_service
from utils.security import role_required

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")


@payment_bp.route("/create-order/<int:order_id>", methods=["GET"])
@login_required
@role_required("BUYER")
def create_order(order_id):
    """Create Razorpay order and show payment page"""
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first_or_404()
    
    # Check if order is in correct state
    if order.status != "PENDING_PAYMENT":
        flash("This order has already been processed.", "warning")
        return redirect(url_for("buyer.dashboard"))
    
    try:
        # Create Razorpay order
        razorpay_order = payment_service.create_razorpay_order(
            amount=order.total_amount,
            currency="INR",
            receipt=order.order_uuid
        )
        
        # Save Razorpay order ID
        order.razorpay_order_id = razorpay_order['id']
        db.session.commit()
        
        # Render payment page with Razorpay details
        return render_template(
            "buyer/payment.html",
            order=order,
            razorpay_order_id=razorpay_order['id'],
            razorpay_key_id=payment_service.client.auth[0] if payment_service.client else None,
            amount=int(order.total_amount * 100)  # Amount in paise
        )
        
    except Exception as e:
        flash(f"Failed to create payment order: {str(e)}", "error")
        return redirect(url_for("buyer.dashboard"))


@payment_bp.route("/verify", methods=["POST"])
@login_required
@role_required("BUYER")
def verify_payment():
    """Verify Razorpay payment signature and update order status"""
    try:
        # Get payment details from request
        razorpay_order_id = request.form.get("razorpay_order_id")
        razorpay_payment_id = request.form.get("razorpay_payment_id")
        razorpay_signature = request.form.get("razorpay_signature")
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            flash("Invalid payment response.", "error")
            return redirect(url_for("buyer.dashboard"))
        
        # Find order by Razorpay order ID
        order = Order.query.filter_by(razorpay_order_id=razorpay_order_id).first()
        if not order:
            flash("Order not found.", "error")
            return redirect(url_for("buyer.dashboard"))
        
        # Verify signature
        is_valid = payment_service.verify_payment_signature(
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature
        )
        
        if is_valid:
            # Update order status
            order.status = "PAID"
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            
            # Create payment record
            payment = Payment(
                order_id=order.id,
                transaction_status="SUCCESS",
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature
            )
            db.session.add(payment)
            
            # Create blockchain order record
            blockchain_order = BlockchainOrder(
                order_id=order.id,
                state="PAID"
            )
            db.session.add(blockchain_order)
            
            db.session.commit()
            
            # Trigger blockchain transaction to create order on-chain
            from services.blockchain_service import blockchain_service
            
            # Get buyer and farmer wallet addresses (or use defaults)
            buyer_wallet = order.buyer.wallet_address or "0x0000000000000000000000000000000000000000"
            farmer_wallet = order.farmer.wallet_address or "0x0000000000000000000000000000000000000000"
            
            # Convert amount to wei (1 ETH = 10^18 wei, but we'll use a small amount for testing)
            # For real implementation, you'd convert the rupee amount to crypto equivalent
            amount_in_wei = int(order.total_amount * 10**15)  # Example conversion
            
            tx_hash = blockchain_service.create_order_on_chain(
                order.id,
                buyer_wallet,
                farmer_wallet,
                amount_in_wei
            )
            
            if tx_hash:
                blockchain_order.tx_hash_create = tx_hash
                blockchain_order.onchain_order_id = str(order.id)
                db.session.commit()
                print(f"[INFO] Blockchain order created with tx: {tx_hash}")
            
            # TODO: Send notification to farmer
            
            flash("Payment successful! Your order has been placed.", "success")
            return redirect(url_for("payment.success", order_id=order.id))
        else:
            # Payment verification failed
            order.status = "PAYMENT_FAILED"
            
            payment = Payment(
                order_id=order.id,
                transaction_status="FAILED",
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature
            )
            db.session.add(payment)
            db.session.commit()
            
            flash("Payment verification failed. Please try again.", "error")
            return redirect(url_for("payment.failure", order_id=order.id))
            
    except Exception as e:
        flash(f"Payment processing error: {str(e)}", "error")
        return redirect(url_for("buyer.dashboard"))


@payment_bp.route("/success/<int:order_id>")
@login_required
@role_required("BUYER")
def success(order_id):
    """Payment success page"""
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first_or_404()
    return render_template("buyer/payment_success.html", order=order)


@payment_bp.route("/failure/<int:order_id>")
@login_required
@role_required("BUYER")
def failure(order_id):
    """Payment failure page"""
    order = Order.query.filter_by(id=order_id, buyer_id=current_user.id).first_or_404()
    return render_template("buyer/payment_failure.html", order=order)
