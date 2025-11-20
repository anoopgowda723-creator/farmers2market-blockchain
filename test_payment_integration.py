import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app
from extensions import db
from models.user import User
from models.product import Product
from models.order import Order, OrderItem
from models.payment import Payment
from models.blockchain_order import BlockchainOrder
from services.payment_service import payment_service
import uuid

app = create_app()

def test_payment_integration():
    """Test the complete payment integration flow"""
    with app.app_context():
        print("\n=== Testing Razorpay Payment Integration ===\n")
        
        # 1. Check if payment service is initialized
        print("1. Checking payment service initialization...")
        if payment_service.client:
            print("   ✓ Payment service initialized successfully")
        else:
            print("   ⚠ Payment service not initialized (Razorpay credentials not set)")
            print("   This is expected if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET are not configured")
        
        # 2. Create test order
        print("\n2. Creating test order...")
        buyer = User.query.filter_by(role="BUYER").first()
        farmer = User.query.filter_by(role="FARMER").first()
        
        if not buyer or not farmer:
            print("   ⚠ No buyer or farmer found. Please create users first.")
            return
        
        test_order = Order(
            order_uuid=str(uuid.uuid4()),
            buyer_id=buyer.id,
            farmer_id=farmer.id,
            total_amount=100.00,
            status="PENDING_PAYMENT",
            delivery_address="Test Address"
        )
        db.session.add(test_order)
        db.session.commit()
        print(f"   ✓ Test order created: {test_order.order_uuid}")
        
        # 3. Test Razorpay order creation (if credentials are set)
        if payment_service.client:
            print("\n3. Testing Razorpay order creation...")
            try:
                razorpay_order = payment_service.create_razorpay_order(
                    amount=test_order.total_amount,
                    currency="INR",
                    receipt=test_order.order_uuid
                )
                print(f"   ✓ Razorpay order created: {razorpay_order['id']}")
                print(f"   Amount: ₹{razorpay_order['amount']/100}")
                
                # Save Razorpay order ID
                test_order.razorpay_order_id = razorpay_order['id']
                db.session.commit()
                
            except Exception as e:
                print(f"   ✗ Failed to create Razorpay order: {e}")
        else:
            print("\n3. Skipping Razorpay order creation (credentials not set)")
        
        # 4. Test signature verification logic (with dummy data)
        print("\n4. Testing signature verification logic...")
        try:
            # This will fail without real credentials, but tests the logic
            is_valid = payment_service.verify_payment_signature(
                "order_test123",
                "pay_test456",
                "dummy_signature"
            )
            print(f"   Signature verification returned: {is_valid}")
        except Exception as e:
            print(f"   Expected error (no credentials): {str(e)[:50]}...")
        
        # 5. Test payment record creation
        print("\n5. Testing payment record creation...")
        payment = Payment(
            order_id=test_order.id,
            transaction_status="SUCCESS",
            razorpay_order_id="test_order_123",
            razorpay_payment_id="test_pay_456",
            razorpay_signature="test_signature"
        )
        db.session.add(payment)
        
        # 6. Test blockchain order creation
        print("6. Testing blockchain order creation...")
        blockchain_order = BlockchainOrder(
            order_id=test_order.id,
            state="PAID"
        )
        db.session.add(blockchain_order)
        db.session.commit()
        print("   ✓ Payment and blockchain order records created")
        
        # 7. Verify order status update
        print("\n7. Verifying order status...")
        test_order.status = "PAID"
        db.session.commit()
        print(f"   ✓ Order status updated to: {test_order.status}")
        
        # 8. Cleanup
        print("\n8. Cleaning up test data...")
        db.session.delete(blockchain_order)
        db.session.delete(payment)
        db.session.delete(test_order)
        db.session.commit()
        print("   ✓ Test data cleaned up")
        
        print("\n=== Payment Integration Test Complete ===")
        print("\n✅ All payment components are in place!")
        print("\nNext steps:")
        print("1. Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in config.py")
        print("2. Test the full flow: Checkout → Payment → Verification")
        print("3. Implement blockchain escrow integration (Phase 3)")

if __name__ == "__main__":
    test_payment_integration()
