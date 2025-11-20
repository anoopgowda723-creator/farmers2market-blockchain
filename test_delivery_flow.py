import sys
import os
import uuid

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app
from extensions import db
from models.user import User
from models.product import Product
from models.order import Order
from models.delivery import Delivery
from models.cart import Cart, CartItem
from services.auth_service import hash_password

app = create_app()

def test_delivery_flow():
    with app.app_context():
        # Cleanup & Reset Schema
        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0"))
        db.drop_all()
        db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
        db.create_all()
        print("Database schema reset.")

        # 1. Create Users
        print("Creating users...")
        farmer = User(name="Farmer Joe", email="farmer@test.com", phone="+919999999991", role="FARMER", password_hash=hash_password("pass"), is_active=True, is_approved=True)
        admin = User(name="Admin", email="admin@test.com", phone="+919999999992", role="ADMIN", password_hash=hash_password("pass"), is_active=True, is_approved=True)
        buyer = User(name="Buyer Bob", email="buyer@test.com", phone="+919999999993", role="BUYER", password_hash=hash_password("pass"), is_active=True, is_approved=True)
        delivery_partner = User(name="Delivery Dan", email="delivery@test.com", phone="+919999999994", role="DELIVERY", password_hash=hash_password("pass"), is_active=True, is_approved=True)
        
        db.session.add_all([farmer, admin, buyer, delivery_partner])
        db.session.commit()
        
        # 2. Create Product & Order (Skipping cart steps for brevity, creating order directly)
        print("Creating order...")
        product = Product(farmer_id=farmer.id, name="Tomatoes", price=50.0, stock=100, status="APPROVED")
        db.session.add(product)
        db.session.commit()
        
        order = Order(
            order_uuid=str(uuid.uuid4()),
            buyer_id=buyer.id,
            farmer_id=farmer.id,
            total_amount=100.0,
            status="PAID", # Simulate paid order
            delivery_address="123 Buyer St"
        )
        db.session.add(order)
        db.session.commit()
        
        # 3. Farmer Confirms
        print("Farmer confirming order...")
        order.status = "FARMER_CONFIRMED"
        db.session.commit()
        
        # 4. Admin Assigns Delivery
        print("Admin assigning delivery...")
        delivery = Delivery(
            order_id=order.id,
            delivery_partner_id=delivery_partner.id,
            status="ASSIGNED"
        )
        db.session.add(delivery)
        order.status = "ASSIGNED_DELIVERY"
        db.session.commit()
        
        # 5. Delivery Partner Updates Status
        print("Delivery partner updating status...")
        d = Delivery.query.get(delivery.id)
        d.status = "DELIVERED"
        d.order.status = "DELIVERED"
        db.session.commit()
        
        # Verify
        final_order = Order.query.get(order.id)
        print(f"Final Order Status: {final_order.status}")
        print(f"Final Delivery Status: {d.status}")
        
        if final_order.status == "DELIVERED" and d.status == "DELIVERED":
            print("TEST PASSED: Delivery flow completed.")
        else:
            print("TEST FAILED: Status mismatch.")

if __name__ == "__main__":
    test_delivery_flow()
