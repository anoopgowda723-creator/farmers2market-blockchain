import json
import os
from web3 import Web3
from flask import current_app

class BlockchainService:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.enabled = False
        self.system_wallet = None
        self.system_private_key = None

    def init_app(self, app):
        provider_uri = app.config.get("WEB3_PROVIDER_URI")
        if not provider_uri:
            print("[WARN] No WEB3_PROVIDER_URI set. Blockchain disabled.")
            return

        try:
            self.w3 = Web3(Web3.HTTPProvider(provider_uri))
            if self.w3.is_connected():
                print(f"[INFO] Connected to Blockchain at {provider_uri}")
                self.enabled = True
                self._load_contract(app)
                self._load_system_wallet(app)
            else:
                print("[WARN] Could not connect to Blockchain.")
        except Exception as e:
            print(f"[ERROR] Blockchain connection failed: {e}")

    def _load_contract(self, app):
        address = app.config.get("SMART_CONTRACT_ADDRESS")
        abi_path = app.config.get("SMART_CONTRACT_ABI_PATH")

        if not address or not abi_path or not os.path.exists(abi_path):
            print("[WARN] Contract address or ABI not found. Contract calls disabled.")
            return

        try:
            with open(abi_path, "r") as f:
                abi = json.load(f)
            
            self.contract = self.w3.eth.contract(address=address, abi=abi)
            print(f"[INFO] Loaded Smart Contract at {address}")
        except Exception as e:
            print(f"[ERROR] Failed to load contract: {e}")
    
    def _load_system_wallet(self, app):
        """Load system wallet for sending transactions"""
        self.system_wallet = app.config.get("SYSTEM_WALLET_ADDRESS")
        self.system_private_key = app.config.get("SYSTEM_WALLET_PRIVATE_KEY")
        
        if self.system_wallet and self.system_private_key:
            print(f"[INFO] System wallet loaded: {self.system_wallet}")
        else:
            print("[WARN] System wallet not configured. Transactions will be mocked.")

    def create_order_on_chain(self, order_id, buyer_address, farmer_address, amount_in_wei):
        """
        Create order on blockchain escrow
        
        Args:
            order_id: Order ID from database
            buyer_address: Buyer's wallet address
            farmer_address: Farmer's wallet address
            amount_in_wei: Amount in wei to hold in escrow
            
        Returns:
            Transaction hash or None
        """
        if not self.enabled or not self.contract:
            print("[WARN] Blockchain not ready. Mocking createOrder call.")
            return f"0xmocked_{order_id}"

        if not self.system_wallet or not self.system_private_key:
            print("[WARN] System wallet not configured. Mocking transaction.")
            return f"0xmocked_{order_id}"

        try:
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.system_wallet)
            
            tx = self.contract.functions.createOrder(
                int(order_id),
                buyer_address,
                farmer_address
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'value': amount_in_wei
            })
            
            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.system_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = receipt.transactionHash.hex()
            
            print(f"[INFO] Order {order_id} created on-chain: {tx_hash_hex}")
            return tx_hash_hex
            
        except Exception as e:
            print(f"[ERROR] Failed to create order on-chain: {e}")
            return None

    def mark_farmer_confirmed(self, order_id):
        """
        Mark order as confirmed by farmer on blockchain
        
        Args:
            order_id: Order ID
            
        Returns:
            Transaction hash or None
        """
        if not self.enabled or not self.contract:
            print("[WARN] Blockchain not ready. Mocking markFarmerConfirmed call.")
            return f"0xmocked_confirm_{order_id}"

        if not self.system_wallet or not self.system_private_key:
            print("[WARN] System wallet not configured. Mocking transaction.")
            return f"0xmocked_confirm_{order_id}"

        try:
            nonce = self.w3.eth.get_transaction_count(self.system_wallet)
            
            tx = self.contract.functions.markFarmerConfirmed(
                int(order_id)
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.system_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = receipt.transactionHash.hex()
            
            print(f"[INFO] Order {order_id} farmer confirmed on-chain: {tx_hash_hex}")
            return tx_hash_hex
            
        except Exception as e:
            print(f"[ERROR] Failed to mark farmer confirmed: {e}")
            return None

    def mark_out_for_delivery(self, order_id):
        """Mark order as out for delivery on blockchain"""
        if not self.enabled or not self.contract:
            print("[WARN] Blockchain not ready. Mocking markOutForDelivery call.")
            return f"0xmocked_delivery_{order_id}"

        if not self.system_wallet or not self.system_private_key:
            print("[WARN] System wallet not configured. Mocking transaction.")
            return f"0xmocked_delivery_{order_id}"

        try:
            nonce = self.w3.eth.get_transaction_count(self.system_wallet)
            
            tx = self.contract.functions.markOutForDelivery(
                int(order_id)
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.system_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"[INFO] Order {order_id} marked out for delivery on-chain")
            return receipt.transactionHash.hex()
            
        except Exception as e:
            print(f"[ERROR] Failed to mark out for delivery: {e}")
            return None

    def submit_delivery_proof(self, order_id, proof_hash):
        """
        Submit delivery proof to blockchain
        
        Args:
            order_id: Order ID
            proof_hash: Hash of delivery proof (bytes32)
            
        Returns:
            Transaction hash or None
        """
        if not self.enabled or not self.contract:
            print("[WARN] Blockchain not ready. Mocking submitDeliveryProof call.")
            return f"0xmocked_proof_{order_id}"

        if not self.system_wallet or not self.system_private_key:
            print("[WARN] System wallet not configured. Mocking transaction.")
            return f"0xmocked_proof_{order_id}"

        try:
            # Convert proof hash to bytes32 if it's a string
            if isinstance(proof_hash, str):
                if proof_hash.startswith('0x'):
                    proof_hash = bytes.fromhex(proof_hash[2:])
                else:
                    proof_hash = bytes.fromhex(proof_hash)
            
            nonce = self.w3.eth.get_transaction_count(self.system_wallet)
            
            tx = self.contract.functions.submitDeliveryProof(
                int(order_id),
                proof_hash
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 150000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.system_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = receipt.transactionHash.hex()
            
            print(f"[INFO] Delivery proof submitted for order {order_id}: {tx_hash_hex}")
            return tx_hash_hex
            
        except Exception as e:
            print(f"[ERROR] Failed to submit delivery proof: {e}")
            return None

    def release_funds(self, order_id):
        """
        Release funds from escrow to farmer
        
        Args:
            order_id: Order ID
            
        Returns:
            Transaction hash or None
        """
        if not self.enabled or not self.contract:
            print("[WARN] Blockchain not ready. Mocking releaseFunds call.")
            return f"0xmocked_release_{order_id}"

        if not self.system_wallet or not self.system_private_key:
            print("[WARN] System wallet not configured. Mocking transaction.")
            return f"0xmocked_release_{order_id}"

        try:
            nonce = self.w3.eth.get_transaction_count(self.system_wallet)
            
            tx = self.contract.functions.releaseFunds(
                int(order_id)
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.system_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = receipt.transactionHash.hex()
            
            print(f"[INFO] Funds released for order {order_id}: {tx_hash_hex}")
            return tx_hash_hex
            
        except Exception as e:
            print(f"[ERROR] Failed to release funds: {e}")
            return None

    def refund_buyer(self, order_id):
        """
        Refund buyer from escrow
        
        Args:
            order_id: Order ID
            
        Returns:
            Transaction hash or None
        """
        if not self.enabled or not self.contract:
            print("[WARN] Blockchain not ready. Mocking refundBuyer call.")
            return f"0xmocked_refund_{order_id}"

        if not self.system_wallet or not self.system_private_key:
            print("[WARN] System wallet not configured. Mocking transaction.")
            return f"0xmocked_refund_{order_id}"

        try:
            nonce = self.w3.eth.get_transaction_count(self.system_wallet)
            
            tx = self.contract.functions.refundBuyer(
                int(order_id)
            ).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.system_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_hash_hex = receipt.transactionHash.hex()
            
            print(f"[INFO] Buyer refunded for order {order_id}: {tx_hash_hex}")
            return tx_hash_hex
            
        except Exception as e:
            print(f"[ERROR] Failed to refund buyer: {e}")
            return None

    def generate_hash(self, data):
        """Generate Keccak256 hash of data"""
        return Web3.keccak(text=data).hex()

# Singleton
blockchain_service = BlockchainService()
