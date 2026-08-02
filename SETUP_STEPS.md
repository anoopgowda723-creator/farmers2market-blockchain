## 🚀 Ganache Blockchain Setup - Step-by-Step Execution Guide

### ✅ Step 1: Dependencies Installed
- `py-solc-x` - Solidity compiler for Python
- `python-dotenv` - Environment variable management

---

### 📋 Next Steps to Complete Setup:

#### Step 2: Start Ganache (REQUIRED - Do this first!)

**Open a NEW terminal window** and run:
```bash
ganache --port 8545 --deterministic
```

**IMPORTANT:** 
- Keep this terminal window open while developing
- You'll see 10 accounts with addresses and private keys
- **Copy the FIRST private key** (account 0) - you'll need it later!

Example output you'll see:
```
Available Accounts
==================
(0) 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 (1000 ETH)
...

Private Keys
==================
(0) 0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
```

**👉 Copy this private key! You'll need it in Step 5.**

---

#### Step 3: Compile Smart Contract

Once Ganache is running, compile the contract:
```bash
cd c:\farmer_market
python scripts\compile_contract.py
```

Expected output:
```
✅ Contract compiled successfully!
💾 Saved to: backend/contracts/OrderEscrow.json
```

---

#### Step 4: Deploy Contract to Ganache

Deploy the compiled contract:
```bash
python scripts\deploy_contract.py
```

Expected output:
```
✅ Contract deployed successfully!
📍 Contract Address: 0x...
💾 Configuration saved to: .env
```

---

#### Step 5: Add Private Key to .env

1. Open the `.env` file in your project root
2. Find this line:
   ```
   # SYSTEM_WALLET_PRIVATE_KEY=0x...
   ```
3. Replace it with the private key from Step 2:
   ```
   SYSTEM_WALLET_PRIVATE_KEY=0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
   ```
   (Use YOUR actual key from Ganache)

---

#### Step 6: Test Blockchain Connection

Verify everything is working:
```bash
python scripts\test_blockchain_connection.py
```

Expected output:
```
✅ Connected successfully!
📊 Network Information
✅ Contract loaded successfully!
```

---

#### Step 7: Test Contract Functions

Run comprehensive contract tests:
```bash
python scripts\test_contract_interaction.py
```

This will test:
- ✅ Creating orders
- ✅ Farmer confirmation
- ✅ Delivery tracking
- ✅ Fund release

---

#### Step 8: Start Your Backend

Finally, start your Flask application:
```bash
cd backend
python app.py
```

Look for these messages in the console:
```
[INFO] Connected to Blockchain at http://127.0.0.1:8545
[INFO] Loaded Smart Contract at 0x...
[INFO] System wallet loaded: 0x...
```

---

### 🎉 Success!

If you see all the above messages, your blockchain integration is ready!

You can now:
- Place orders through your web interface
- See blockchain transactions in the Ganache terminal
- Track escrow payments and fund releases
- Test the complete order lifecycle with blockchain verification

---

### 🆘 Troubleshooting

**"Connection Refused"**
- Make sure Ganache is running in a separate terminal
- Check it's on port 8545

**"Contract not found"**
- Run the compilation script again
- Make sure `backend/contracts/OrderEscrow.json` exists

**"Invalid private key"**
- Check you copied the full private key from Ganache
- Make sure it starts with `0x`
- No spaces or extra characters

---

### 📞 Need Help?

Refer to:
- `GANACHE_SETUP_GUIDE.md` - Full detailed guide
- `QUICK_START.md` - Quick reference
- Ganache terminal output - Shows all transactions

**Ready to start? Begin with Step 2!** 🚀
