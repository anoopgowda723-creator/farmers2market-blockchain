# Quick Start Guide - Ganache Blockchain Setup

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Python Dependencies
```bash
cd c:\farmer_market\backend
pip install py-solc-x python-dotenv
```

### Step 2: Start Ganache
**Open a new terminal** and run:
```bash
cd c:\farmer_market
ganache --port 8545 --deterministic
```

**Keep this terminal open!** You should see:
- 10 accounts with addresses
- Private keys for each account
- Listening on http://127.0.0.1:8545

**IMPORTANT:** Copy the first private key (account 0) - you'll need it in Step 4!

### Step 3: Compile & Deploy Contract
**In a second terminal:**
```bash
cd c:\farmer_market

# Compile the smart contract
python scripts\compile_contract.py

# Deploy to Ganache
python scripts\deploy_contract.py
```

### Step 4: Add Private Key to .env
1. Open `.env` file in the project root
2. Find the line: `# SYSTEM_WALLET_PRIVATE_KEY=0x...`
3. Replace it with the private key from Step 2:
   ```
   SYSTEM_WALLET_PRIVATE_KEY=0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
   ```
   (Use the actual key from your Ganache output)

### Step 5: Test Everything
```bash
# Test blockchain connection
python scripts\test_blockchain_connection.py

# Test contract functions
python scripts\test_contract_interaction.py
```

### Step 6: Start Your Backend
```bash
cd backend
python app.py
```

## ✅ Success Indicators

You're all set if you see:
- ✅ Ganache running on port 8545
- ✅ Contract deployed with an address
- ✅ All tests passing
- ✅ Backend connects to blockchain

## 🎯 Daily Workflow

1. **Start Ganache** (Terminal 1)
   ```bash
   ganache --port 8545 --deterministic
   ```

2. **Start Backend** (Terminal 2)
   ```bash
   cd backend
   python app.py
   ```

3. **Test features** through your web interface

## 🆘 Troubleshooting

### "Connection Refused"
- Make sure Ganache is running
- Check it's on port 8545

### "Invalid Address"
- Run `python scripts\deploy_contract.py` again
- Check `.env` has `SMART_CONTRACT_ADDRESS`

### "Insufficient Funds"
- Restart Ganache to reset balances

## 📚 Full Documentation

See `GANACHE_SETUP_GUIDE.md` for detailed information.

## 🧪 Testing Blockchain Features

Once everything is running, you can:
1. Place an order through the web interface
2. Check Ganache terminal for blockchain transactions
3. View transaction hashes in your app
4. Test the full order → payment → delivery → fund release flow

**Happy Coding! 🎉**
