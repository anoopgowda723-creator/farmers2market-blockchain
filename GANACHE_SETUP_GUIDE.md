# Ganache Blockchain Setup Guide for Farmer2Market

This guide will walk you through setting up Ganache for local blockchain development and deploying your smart contracts.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Starting Ganache](#starting-ganache)
3. [Installing Dependencies](#installing-dependencies)
4. [Compiling Smart Contracts](#compiling-smart-contracts)
5. [Deploying Contracts](#deploying-contracts)
6. [Configuring Backend](#configuring-backend)
7. [Testing Blockchain Integration](#testing-blockchain-integration)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

✅ **Already Installed:**
- Node.js and npm
- Ganache CLI (`npm install -g ganache`)
- Python 3.x
- Web3.py (in your virtual environment)

📦 **Still Need to Install:**
- Solidity Compiler (`solc`)

---

## 1. Starting Ganache

### Option A: Quick Start (Default Settings)
```bash
ganache
```

This starts Ganache with:
- Port: `8545`
- Network ID: `1337`
- 10 accounts with 100 ETH each
- Gas Price: 2 gwei
- Gas Limit: 6721975

### Option B: Custom Configuration (Recommended for Development)
```bash
ganache --port 8545 --networkId 1337 --accounts 10 --defaultBalanceEther 1000 --deterministic
```

**Parameters Explained:**
- `--port 8545`: HTTP-RPC server port (matches your config)
- `--networkId 1337`: Network identifier
- `--accounts 10`: Number of accounts to generate
- `--defaultBalanceEther 1000`: Each account starts with 1000 ETH
- `--deterministic`: Same accounts every time (useful for testing)

### Option C: Using the Provided Script
We've created a startup script for you:

```bash
# Windows PowerShell
.\scripts\start_ganache.ps1

# Or run directly
npm run ganache
```

**Keep Ganache running in a separate terminal window!**

---

## 2. Installing Dependencies

### Install Solidity Compiler

**Option A: Using npm (Recommended)**
```bash
npm install -g solc
```

**Option B: Using pip**
```bash
pip install py-solc-x
```

### Verify Installation
```bash
solc --version
```

You should see something like: `Version: 0.8.x`

---

## 3. Compiling Smart Contracts

### Using the Compilation Script

We've created a Python script to compile your contract:

```bash
cd c:\farmer_market
python scripts\compile_contract.py
```

This will:
1. Read `contracts/OrderEscrow.sol`
2. Compile it using solc
3. Generate `backend/contracts/OrderEscrow.json` with ABI and bytecode

### Manual Compilation (Alternative)

```bash
solc --abi --bin --optimize --overwrite -o backend/contracts contracts/OrderEscrow.sol
```

---

## 4. Deploying Contracts

### Using the Deployment Script

```bash
cd c:\farmer_market
python scripts\deploy_contract.py
```

This script will:
1. Connect to Ganache at `http://127.0.0.1:8545`
2. Deploy the OrderEscrow contract
3. Save the contract address to `.env` file
4. Display deployment details

**Expected Output:**
```
🚀 Deploying OrderEscrow Contract...
✅ Contract deployed successfully!
📍 Contract Address: 0x1234567890abcdef...
💾 Saved to .env file
```

### What Happens During Deployment:
- Uses the first Ganache account as the admin
- Deploys the contract to the blockchain
- Waits for transaction confirmation
- Saves contract address for backend use

---

## 5. Configuring Backend

### Update Environment Variables

After deployment, your `.env` file will be created/updated with:

```env
# Blockchain Configuration
WEB3_PROVIDER_URI=http://127.0.0.1:8545
SMART_CONTRACT_ADDRESS=0x... (your deployed address)
SMART_CONTRACT_ABI_PATH=backend/contracts/OrderEscrow.json

# System Wallet (Admin Account from Ganache)
SYSTEM_WALLET_ADDRESS=0x... (first Ganache account)
SYSTEM_WALLET_PRIVATE_KEY=0x... (private key)
```

### Verify Configuration

Check `backend/config.py`:
```python
WEB3_PROVIDER_URI = os.environ.get("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")
```

The configuration should automatically load from `.env` when you start your Flask app.

---

## 6. Testing Blockchain Integration

### Test 1: Connection Test

```bash
python scripts\test_blockchain_connection.py
```

**Expected Output:**
```
✅ Connected to Ganache
📊 Network ID: 1337
⛽ Latest Block: 5
💰 Admin Balance: 999.99 ETH
```

### Test 2: Contract Interaction Test

```bash
python scripts\test_contract_interaction.py
```

This will test:
- Creating an order on-chain
- Marking farmer confirmed
- Submitting delivery proof
- Releasing funds

### Test 3: Full Integration Test

Start your Flask backend:
```bash
cd backend
python app.py
```

Then run the integration test:
```bash
python test_blockchain_integration.py
```

---

## 7. Common Ganache Commands

### View Accounts
When Ganache starts, it displays 10 accounts with their addresses and private keys:

```
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
```

### Check Transaction History
Ganache logs all transactions in the terminal. Look for:
- `eth_sendRawTransaction`
- `eth_getTransactionReceipt`
- Contract function calls

### Reset Blockchain
To start fresh:
1. Stop Ganache (Ctrl+C)
2. Restart with the same command
3. Re-deploy your contracts

---

## 8. Troubleshooting

### Issue: "Connection Refused" Error

**Problem:** Backend can't connect to Ganache

**Solution:**
1. Ensure Ganache is running: `ganache --port 8545`
2. Check the port in config: `WEB3_PROVIDER_URI=http://127.0.0.1:8545`
3. Verify firewall isn't blocking port 8545

### Issue: "Invalid Address" Error

**Problem:** Contract address not set

**Solution:**
1. Run deployment script: `python scripts\deploy_contract.py`
2. Check `.env` file has `SMART_CONTRACT_ADDRESS`
3. Restart Flask backend

### Issue: "Insufficient Funds" Error

**Problem:** System wallet doesn't have enough ETH

**Solution:**
1. Check Ganache account balances
2. Ensure you're using the correct private key
3. Restart Ganache to reset balances

### Issue: "Nonce Too Low" Error

**Problem:** Transaction nonce mismatch

**Solution:**
1. Restart Ganache (resets nonce)
2. Or wait for pending transactions to complete

### Issue: Contract Compilation Fails

**Problem:** Solidity version mismatch

**Solution:**
1. Check contract pragma: `pragma solidity ^0.8.0;`
2. Install matching solc version: `npm install -g solc@0.8.x`
3. Verify: `solc --version`

---

## 9. Development Workflow

### Daily Development Routine:

1. **Start Ganache** (Terminal 1)
   ```bash
   ganache --port 8545 --deterministic
   ```

2. **Deploy Contracts** (if needed)
   ```bash
   python scripts\deploy_contract.py
   ```

3. **Start Backend** (Terminal 2)
   ```bash
   cd backend
   python app.py
   ```

4. **Test Features**
   - Place orders through the web interface
   - Check Ganache terminal for blockchain transactions
   - Monitor transaction hashes and gas usage

5. **Reset When Needed**
   - Restart Ganache to clear all data
   - Re-deploy contracts
   - Restart backend

---

## 10. Next Steps

Once Ganache is running successfully:

✅ **Integration Testing:**
- Test order creation with blockchain escrow
- Test payment processing
- Test delivery confirmation and fund release

✅ **Frontend Integration:**
- Display transaction hashes in UI
- Show blockchain confirmation status
- Add wallet connection for buyers/farmers

✅ **Production Preparation:**
- Switch to testnet (Sepolia, Goerli)
- Use MetaMask for real wallet integration
- Deploy to mainnet when ready

---

## Quick Reference

| Task | Command |
|------|---------|
| Start Ganache | `ganache --port 8545 --deterministic` |
| Compile Contract | `python scripts\compile_contract.py` |
| Deploy Contract | `python scripts\deploy_contract.py` |
| Test Connection | `python scripts\test_blockchain_connection.py` |
| Start Backend | `cd backend && python app.py` |
| View Logs | Check Ganache terminal output |

---

## Support

If you encounter issues:
1. Check Ganache terminal for error messages
2. Review Flask backend logs
3. Verify all environment variables are set
4. Ensure all dependencies are installed

**Happy Blockchain Development! 🚀**
