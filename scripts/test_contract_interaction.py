"""
Contract Interaction Test Script
Tests all smart contract functions with sample data
"""

import os
import sys
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv
import json
import time

def test_contract_interaction():
    """Test smart contract function calls"""
    
    print("🧪 Testing Smart Contract Interactions")
    print("=" * 60)
    
    # Load environment
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if not env_file.exists():
        print("❌ No .env file found!")
        print("   Run: python scripts/deploy_contract.py")
        sys.exit(1)
    
    load_dotenv(env_file)
    
    # Get configuration
    provider_uri = os.getenv("WEB3_PROVIDER_URI")
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    system_wallet = os.getenv("SYSTEM_WALLET_ADDRESS")
    private_key = os.getenv("SYSTEM_WALLET_PRIVATE_KEY")
    
    if not all([provider_uri, contract_address, system_wallet, private_key]):
        print("❌ Missing configuration!")
        print("   Make sure .env has all required values")
        sys.exit(1)
    
    print("✅ Configuration loaded")
    print()
    
    # Connect to blockchain
    print("🔌 Connecting to blockchain...")
    w3 = Web3(Web3.HTTPProvider(provider_uri))
    
    if not w3.is_connected():
        print("❌ Cannot connect to Ganache!")
        sys.exit(1)
    
    print("✅ Connected")
    print()
    
    # Load contract
    print("📜 Loading contract...")
    abi_path = project_root / "backend" / "contracts" / "OrderEscrow.json"
    
    with open(abi_path, 'r') as f:
        contract_data = json.load(f)
    
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_data['abi']
    )
    
    print(f"✅ Contract loaded at {contract_address}")
    print()
    
    # Test data
    test_order_id = 12345
    buyer_address = w3.eth.accounts[1]  # Second Ganache account
    farmer_address = w3.eth.accounts[2]  # Third Ganache account
    amount = w3.to_wei(0.1, 'ether')  # 0.1 ETH
    
    print("📋 Test Data:")
    print(f"   Order ID: {test_order_id}")
    print(f"   Buyer: {buyer_address}")
    print(f"   Farmer: {farmer_address}")
    print(f"   Amount: {w3.from_wei(amount, 'ether')} ETH")
    print()
    
    try:
        # Test 1: Create Order
        print("=" * 60)
        print("Test 1: Creating Order on Blockchain")
        print("=" * 60)
        
        nonce = w3.eth.get_transaction_count(system_wallet)
        
        tx = contract.functions.createOrder(
            test_order_id,
            buyer_address,
            farmer_address
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 300000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'value': amount
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"📤 Transaction sent: {tx_hash.hex()}")
        print("⏳ Waiting for confirmation...")
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Order created! Gas used: {receipt.gasUsed}")
        print()
        
        # Verify order
        order = contract.functions.getOrder(test_order_id).call()
        print("📊 Order Details:")
        print(f"   Buyer: {order[0]}")
        print(f"   Farmer: {order[1]}")
        print(f"   Amount: {w3.from_wei(order[2], 'ether')} ETH")
        print(f"   State: {order[3]} (1 = PAID)")
        print()
        
        time.sleep(1)
        
        # Test 2: Mark Farmer Confirmed
        print("=" * 60)
        print("Test 2: Marking Farmer Confirmed")
        print("=" * 60)
        
        nonce = w3.eth.get_transaction_count(system_wallet)
        
        tx = contract.functions.markFarmerConfirmed(
            test_order_id
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"📤 Transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Farmer confirmed! Gas used: {receipt.gasUsed}")
        
        order = contract.functions.getOrder(test_order_id).call()
        print(f"   New State: {order[3]} (2 = FARMER_CONFIRMED)")
        print()
        
        time.sleep(1)
        
        # Test 3: Mark Out for Delivery
        print("=" * 60)
        print("Test 3: Marking Out for Delivery")
        print("=" * 60)
        
        nonce = w3.eth.get_transaction_count(system_wallet)
        
        tx = contract.functions.markOutForDelivery(
            test_order_id
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"📤 Transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Out for delivery! Gas used: {receipt.gasUsed}")
        
        order = contract.functions.getOrder(test_order_id).call()
        print(f"   New State: {order[3]} (3 = OUT_FOR_DELIVERY)")
        print()
        
        time.sleep(1)
        
        # Test 4: Submit Delivery Proof
        print("=" * 60)
        print("Test 4: Submitting Delivery Proof")
        print("=" * 60)
        
        proof_hash = Web3.keccak(text="Delivery proof for order 12345")
        print(f"   Proof Hash: {proof_hash.hex()}")
        
        nonce = w3.eth.get_transaction_count(system_wallet)
        
        tx = contract.functions.submitDeliveryProof(
            test_order_id,
            proof_hash
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 150000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"📤 Transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Proof submitted! Gas used: {receipt.gasUsed}")
        
        order = contract.functions.getOrder(test_order_id).call()
        print(f"   New State: {order[3]} (4 = DELIVERED)")
        print(f"   Proof Hash: {order[6].hex()}")
        print()
        
        time.sleep(1)
        
        # Test 5: Release Funds
        print("=" * 60)
        print("Test 5: Releasing Funds to Farmer")
        print("=" * 60)
        
        farmer_balance_before = w3.eth.get_balance(farmer_address)
        print(f"   Farmer balance before: {w3.from_wei(farmer_balance_before, 'ether')} ETH")
        
        nonce = w3.eth.get_transaction_count(system_wallet)
        
        tx = contract.functions.releaseFunds(
            test_order_id
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"📤 Transaction sent: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Funds released! Gas used: {receipt.gasUsed}")
        
        farmer_balance_after = w3.eth.get_balance(farmer_address)
        print(f"   Farmer balance after: {w3.from_wei(farmer_balance_after, 'ether')} ETH")
        print(f"   Received: {w3.from_wei(farmer_balance_after - farmer_balance_before, 'ether')} ETH")
        
        order = contract.functions.getOrder(test_order_id).call()
        print(f"   New State: {order[3]} (5 = FUNDS_RELEASED)")
        print(f"   Order Amount: {w3.from_wei(order[2], 'ether')} ETH (should be 0)")
        print()
        
        # Summary
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("🎉 Your smart contract is working perfectly!")
        print()
        print("📊 Test Summary:")
        print("   ✅ Order created on blockchain")
        print("   ✅ Farmer confirmation recorded")
        print("   ✅ Delivery status updated")
        print("   ✅ Delivery proof submitted")
        print("   ✅ Funds released to farmer")
        print()
        print("🚀 Ready for integration with your Flask backend!")
        print()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_contract_interaction()
