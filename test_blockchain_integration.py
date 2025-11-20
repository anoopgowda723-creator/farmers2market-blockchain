import sys
import os
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app
from services.blockchain_service import blockchain_service

app = create_app()

def test_blockchain_service():
    with app.app_context():
        print("Testing Blockchain Service...")
        
        # 1. Test Hashing
        data = "test-proof-data"
        hash_val = blockchain_service.generate_hash(data)
        print(f"Generated Hash: {hash_val}")
        
        if hash_val and hash_val.startswith("0x"):
            print("Hashing works.")
        else:
            print("Hashing failed.")
            
        # 2. Test Store Proof (Mocked)
        # Enable service manually for testing
        blockchain_service.enabled = True
        blockchain_service.w3 = MagicMock()
        blockchain_service.contract = MagicMock()
        
        # Mock transaction receipt
        mock_receipt = MagicMock()
        mock_receipt.transactionHash.hex.return_value = "0x1234567890abcdef"
        blockchain_service.w3.eth.wait_for_transaction_receipt.return_value = mock_receipt
        
        tx_hash = blockchain_service.store_proof(1, hash_val, "0xSender", "0xKey")
        print(f"Store Proof Tx: {tx_hash}")
        
        if tx_hash == "0x1234567890abcdef":
            print("TEST PASSED: Blockchain service logic verified.")
        else:
            print("TEST FAILED: Store proof logic failed.")

if __name__ == "__main__":
    test_blockchain_service()
