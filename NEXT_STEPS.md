## ✅ Virtual Environment Setup Complete!

### Current Status:
- ✅ Virtual environment activated (`venv`)
- ✅ Flask installed (3.1.2)
- ✅ web3 installed (7.14.0)
- ✅ py-solc-x installed (2.0.4)
- ✅ python-dotenv installed (1.2.1)

---

## 🚀 Next Steps - Follow in Order:

### Step 1: Start Ganache (CRITICAL - Do this first!)

**Open a SECOND terminal window** (keep the current one open) and run:

```powershell
ganache --port 8545 --deterministic
```

**What you'll see:**
```
Ganache CLI v7.9.0 (ganache-core: 2.13.2)

Available Accounts
==================
(0) 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 (1000 ETH)
(1) 0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0 (1000 ETH)
...

Private Keys
==================
(0) 0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
(1) 0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1
...

Listening on 127.0.0.1:8545
```

**⚠️ IMPORTANT:** 
- **Copy the FIRST private key** (the one for account 0)
- Keep this terminal window open!
- You'll need this private key in Step 4

---

### Step 2: Compile the Smart Contract

**In your current terminal** (with venv activated), run:

```powershell
cd c:\farmer_market
python scripts\compile_contract.py
```

**Expected Output:**
```
🔨 Compiling OrderEscrow Smart Contract...
✅ Contract compiled successfully!
💾 Saved to: backend/contracts/OrderEscrow.json
📊 Contract Details:
   - Functions: 10
   - Events: 6
   - Bytecode size: XXXX bytes
✅ Ready for deployment!
```

---

### Step 3: Deploy Contract to Ganache

```powershell
python scripts\deploy_contract.py
```

**Expected Output:**
```
🚀 Deploying OrderEscrow Contract to Ganache
✅ Connected to Ganache
👤 Admin Account: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1
📤 Deploying contract...
✅ Contract deployed successfully!
📍 Contract Address: 0x5FbDB2315678afecb367f032d93F642f64180aa3
💾 Configuration saved to: .env
```

---

### Step 4: Add Private Key to .env File

1. Open the `.env` file in your project root (`c:\farmer_market\.env`)
2. Find this line:
   ```
   # SYSTEM_WALLET_PRIVATE_KEY=0x...
   ```
3. Replace it with the private key you copied from Step 1:
   ```
   SYSTEM_WALLET_PRIVATE_KEY=0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d
   ```
   (Use YOUR actual key from Ganache, not this example)

4. Remove the `#` at the beginning to uncomment it

---

### Step 5: Test Blockchain Connection

```powershell
python scripts\test_blockchain_connection.py
```

**Expected Output:**
```
🧪 Testing Blockchain Connection
✅ Connected successfully!
📊 Network Information:
   Network ID: 1337
   Latest Block: 2
👥 Available Accounts:
   (0) 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 (Admin)
       Balance: 999.99 ETH
📜 Testing Smart Contract...
✅ Contract loaded successfully!
   Admin: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1
   Contract Balance: 0.0 ETH
```

---

### Step 6: Test Contract Functions

```powershell
python scripts\test_contract_interaction.py
```

**Expected Output:**
```
🧪 Testing Smart Contract Interactions
Test 1: Creating Order on Blockchain
✅ Order created! Gas used: 245678
Test 2: Marking Farmer Confirmed
✅ Farmer confirmed! Gas used: 45123
...
✅ ALL TESTS PASSED!
🎉 Your smart contract is working perfectly!
```

---

### Step 7: Start Your Flask Backend

```powershell
cd backend
python app.py
```

**Look for these messages:**
```
[INFO] Connected to Blockchain at http://127.0.0.1:8545
[INFO] Loaded Smart Contract at 0x5FbDB2315678afecb367f032d93F642f64180aa3
[INFO] System wallet loaded: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1
 * Running on http://127.0.0.1:5000
```

---

## 🎉 Success Indicators

You're all set when you see:
- ✅ Ganache running in separate terminal
- ✅ Contract compiled and deployed
- ✅ All tests passing
- ✅ Backend shows blockchain connection messages
- ✅ No errors in console

---

## 🆘 Quick Troubleshooting

**"Connection Refused"**
→ Start Ganache first: `ganache --port 8545 --deterministic`

**"Module not found"**
→ Activate venv: `.\venv\Scripts\Activate.ps1`

**"Invalid private key"**
→ Check `.env` file has the correct key from Ganache (starts with `0x`)

**"Contract not found"**
→ Run compilation script: `python scripts\compile_contract.py`

---

## 📋 Command Summary (Copy-Paste Ready)

```powershell
# Terminal 1: Start Ganache (keep open)
ganache --port 8545 --deterministic

# Terminal 2: Setup (with venv activated)
cd c:\farmer_market
python scripts\compile_contract.py
python scripts\deploy_contract.py
# (Add private key to .env)
python scripts\test_blockchain_connection.py
python scripts\test_contract_interaction.py
cd backend
python app.py
```

---

**Ready to start? Open a new terminal for Ganache (Step 1)!** 🚀
