"""
Blockchain Connection Test Script
Tests connection to Ganache and verifies configuration
"""

import os
import sys
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv

def test_connection():
    """Test blockchain connection and configuration"""
    
    print("🧪 Testing Blockchain Connection")
    print("=" * 60)
    
    # Load environment variables
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if env_file.exists():
        load_dotenv(env_file)
        print("✅ Loaded .env file")
    else:
        print("⚠️  No .env file found, using defaults")
    
    print()
    
    # Get configuration
    provider_uri = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    system_wallet = os.getenv("SYSTEM_WALLET_ADDRESS")
    
    print("📋 Configuration:")
    print(f"   Provider: {provider_uri}")
    print(f"   Contract: {contract_address or 'Not set'}")
    print(f"   Wallet: {system_wallet or 'Not set'}")
    print()
    
    # Test connection
    print("🔌 Connecting to blockchain...")
    try:
        w3 = Web3(Web3.HTTPProvider(provider_uri))
        
        if not w3.is_connected():
            print("❌ Connection failed!")
            print()
            print("Make sure Ganache is running:")
            print("   ganache --port 8545 --deterministic")
            sys.exit(1)
        
        print("✅ Connected successfully!")
        print()
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        sys.exit(1)
    
    # Get network info
    print("📊 Network Information:")
    print(f"   Network ID: {w3.eth.chain_id}")
    print(f"   Latest Block: {w3.eth.block_number}")
    print(f"   Gas Price: {w3.from_wei(w3.eth.gas_price, 'gwei')} gwei")
    print()
    
    # Check accounts
    print("👥 Available Accounts:")
    accounts = w3.eth.accounts
    for i, account in enumerate(accounts[:5]):  # Show first 5
        balance = w3.eth.get_balance(account)
        balance_eth = w3.from_wei(balance, 'ether')
        marker = " (Admin)" if account == system_wallet else ""
        print(f"   ({i}) {account}{marker}")
        print(f"       Balance: {balance_eth} ETH")
    
    if len(accounts) > 5:
        print(f"   ... and {len(accounts) - 5} more accounts")
    print()
    
    # Test contract if address is set
    if contract_address:
        print("📜 Testing Smart Contract...")
        
        abi_path = project_root / "backend" / "contracts" / "OrderEscrow.json"
        if not abi_path.exists():
            print("⚠️  Contract ABI not found")
            print(f"   Expected at: {abi_path}")
        else:
            try:
                import json
                with open(abi_path, 'r') as f:
                    contract_data = json.load(f)
                
                contract = w3.eth.contract(
                    address=contract_address,
                    abi=contract_data['abi']
                )
                
                # Test contract calls
                admin = contract.functions.admin().call()
                balance = contract.functions.getBalance().call()
                
                print(f"✅ Contract loaded successfully!")
                print(f"   Admin: {admin}")
                print(f"   Contract Balance: {w3.from_wei(balance, 'ether')} ETH")
                print()
                
            except Exception as e:
                print(f"⚠️  Contract test failed: {e}")
                print()
    else:
        print("⚠️  No contract address configured")
        print("   Run: python scripts/deploy_contract.py")
        print()
    
    # Summary
    print("=" * 60)
    print("✅ CONNECTION TEST COMPLETE!")
    print("=" * 60)
    print()
    
    if contract_address:
        print("🎉 Everything looks good! Your blockchain is ready.")
    else:
        print("📋 Next step: Deploy your contract")
        print("   python scripts/deploy_contract.py")
    print()

if __name__ == "__main__":
    test_connection()
