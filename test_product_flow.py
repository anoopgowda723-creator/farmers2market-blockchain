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
from models.cart import Cart, CartItem
from services.auth_service import hash_password

app = create_app()

def test_product_flow():
    with app.app_context():
        # Cleanup
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
        
        db.session.add_all([farmer, admin, buyer])
        db.session.commit()
        
        # 2. Farmer creates product
        print("Farmer creating product...")
        product = Product(
            farmer_id=farmer.id,
            name="Fresh Tomatoes",
            description="Red and juicy",
            price=50.0,
            stock=100,
            status="PENDING_APPROVAL"
        )
        db.session.add(product)
        db.session.commit()
        
        # 3. Admin approves product
        print("Admin approving product...")
        p = Product.query.get(product.id)
        p.status = "APPROVED"
        db.session.commit()
        
        # 4. Buyer adds to cart
        print("Buyer adding to cart...")
        cart = Cart(user_id=buyer.id)
        db.session.add(cart)
        db.session.commit()
        
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=2, unit_price=product.price)
        db.session.add(cart_item)
        db.session.commit()
        
        # 5. Checkout (Simulate logic from buyer_routes.checkout)
        print("Buyer checking out...")
        total_amount = cart_item.quantity * cart_item.unit_price
        order = Order(
            order_uuid=str(uuid.uuid4()),
            buyer_id=buyer.id,
            farmer_id=farmer.id,
            total_amount=total_amount,
            status="PENDING_PAYMENT",
            delivery_address="123 Buyer St"
        )
        db.session.add(order)
        db.session.commit()
        
        print(f"Order created: {order.id}, Status: {order.status}")
        
        if order.id:
            print("TEST PASSED: Product flow completed.")
        else:
            print("TEST FAILED: Order not created.")

if __name__ == "__main__":
    test_product_flow()
