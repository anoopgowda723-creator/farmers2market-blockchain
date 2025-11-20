import razorpay
import hmac
import hashlib
from flask import current_app


class PaymentService:
    """Service for handling Razorpay payment operations"""
    
    def __init__(self):
        self.client = None
    
    def init_app(self, app):
        """Initialize Razorpay client with app config"""
        key_id = app.config.get('RAZORPAY_KEY_ID')
        key_secret = app.config.get('RAZORPAY_KEY_SECRET')
        
        if key_id and key_secret:
            self.client = razorpay.Client(auth=(key_id, key_secret))
            print(f"[INFO] Razorpay client initialized")
        else:
            print("[WARN] Razorpay credentials not configured. Payment features will not work.")
    
    def create_razorpay_order(self, amount, currency='INR', receipt=None):
        """
        Create a Razorpay order
        
        Args:
            amount: Amount in smallest currency unit (paise for INR)
            currency: Currency code (default: INR)
            receipt: Optional receipt ID for reference
            
        Returns:
            dict: Razorpay order response with order_id, amount, currency, etc.
        """
        if not self.client:
            raise Exception("Razorpay client not initialized. Check credentials.")
        
        try:
            order_data = {
                'amount': int(amount * 100),  # Convert to paise
                'currency': currency,
                'receipt': receipt or f'order_{amount}',
                'payment_capture': 1  # Auto capture payment
            }
            
            order = self.client.order.create(data=order_data)
            print(f"[INFO] Razorpay order created: {order['id']}")
            return order
            
        except Exception as e:
            print(f"[ERROR] Failed to create Razorpay order: {e}")
            raise
    
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """
        Verify Razorpay payment signature
        
        Args:
            razorpay_order_id: Order ID from Razorpay
            razorpay_payment_id: Payment ID from Razorpay
            razorpay_signature: Signature from Razorpay
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not self.client:
            raise Exception("Razorpay client not initialized. Check credentials.")
        
        try:
            # Generate expected signature
            key_secret = current_app.config.get('RAZORPAY_KEY_SECRET')
            message = f"{razorpay_order_id}|{razorpay_payment_id}"
            
            generated_signature = hmac.new(
                key_secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            is_valid = hmac.compare_digest(generated_signature, razorpay_signature)
            
            if is_valid:
                print(f"[INFO] Payment signature verified for order: {razorpay_order_id}")
            else:
                print(f"[WARN] Invalid payment signature for order: {razorpay_order_id}")
            
            return is_valid
            
        except Exception as e:
            print(f"[ERROR] Failed to verify payment signature: {e}")
            return False
    
    def fetch_payment(self, payment_id):
        """
        Fetch payment details from Razorpay
        
        Args:
            payment_id: Razorpay payment ID
            
        Returns:
            dict: Payment details
        """
        if not self.client:
            raise Exception("Razorpay client not initialized.")
        
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment
        except Exception as e:
            print(f"[ERROR] Failed to fetch payment {payment_id}: {e}")
            raise
    
    def refund_payment(self, payment_id, amount=None):
        """
        Refund a payment
        
        Args:
            payment_id: Razorpay payment ID
            amount: Amount to refund in paise (None for full refund)
            
        Returns:
            dict: Refund details
        """
        if not self.client:
            raise Exception("Razorpay client not initialized.")
        
        try:
            refund_data = {}
            if amount:
                refund_data['amount'] = int(amount * 100)
            
            refund = self.client.payment.refund(payment_id, refund_data)
            print(f"[INFO] Refund initiated for payment {payment_id}")
            return refund
            
        except Exception as e:
            print(f"[ERROR] Failed to refund payment {payment_id}: {e}")
            raise


# Singleton instance
payment_service = PaymentService()
