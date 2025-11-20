# Smart Contract Deployment Guide

## OrderEscrow.sol Deployment

This guide explains how to deploy the `OrderEscrow.sol` smart contract to a blockchain network.

## Prerequisites

1. **Node.js & npm** installed
2. **Hardhat** or **Truffle** (we'll use Hardhat)
3. **MetaMask** wallet with testnet ETH
4. **Infura** or **Alchemy** account (for testnet deployment)

## Option 1: Deploy to Local Ganache (Development)

### Step 1: Install Ganache
```bash
npm install -g ganache
```

### Step 2: Start Ganache
```bash
ganache --port 8545
```

This will give you 10 test accounts with 100 ETH each.

### Step 3: Install Hardhat
```bash
cd C:\farmer_market
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat
```

Select "Create a JavaScript project"

### Step 4: Configure Hardhat

Edit `hardhat.config.js`:
```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.0",
  networks: {
    ganache: {
      url: "http://127.0.0.1:8545",
      accounts: ["0xYOUR_PRIVATE_KEY_FROM_GANACHE"]
    }
  }
};
```

### Step 5: Move Contract
```bash
mv contracts/OrderEscrow.sol contracts/
```

### Step 6: Create Deployment Script

Create `scripts/deploy.js`:
```javascript
async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with:", deployer.address);

  const OrderEscrow = await ethers.getContractFactory("OrderEscrow");
  const escrow = await OrderEscrow.deploy();
  await escrow.deployed();

  console.log("OrderEscrow deployed to:", escrow.address);
  
  // Save ABI and address
  const fs = require('fs');
  const contractData = {
    address: escrow.address,
    abi: JSON.parse(escrow.interface.format('json'))
  };
  
  fs.writeFileSync(
    '../backend/contracts/OrderEscrow.json',
    JSON.stringify(contractData, null, 2)
  );
  
  console.log("ABI saved to backend/contracts/OrderEscrow.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### Step 7: Deploy
```bash
npx hardhat run scripts/deploy.js --network ganache
```

### Step 8: Update Backend Config

In `backend/config.py`:
```python
SMART_CONTRACT_ADDRESS = "0xYOUR_DEPLOYED_ADDRESS"
SMART_CONTRACT_ABI_PATH = os.path.join(BASE_DIR, "contracts", "OrderEscrow.json")
SYSTEM_WALLET_ADDRESS = "0xYOUR_GANACHE_ACCOUNT"
SYSTEM_WALLET_PRIVATE_KEY = "0xYOUR_GANACHE_PRIVATE_KEY"
WEB3_PROVIDER_URI = "http://127.0.0.1:8545"
```

---

## Option 2: Deploy to Ethereum Testnet (Sepolia/Goerli)

### Step 1: Get Testnet ETH
- Go to https://sepoliafaucet.com/
- Enter your MetaMask address
- Get free testnet ETH

### Step 2: Get Infura/Alchemy API Key
- Sign up at https://infura.io/ or https://alchemy.com/
- Create a new project
- Copy your API key

### Step 3: Configure Hardhat for Testnet

Edit `hardhat.config.js`:
```javascript
require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

module.exports = {
  solidity: "0.8.0",
  networks: {
    sepolia: {
      url: `https://sepolia.infura.io/v3/${process.env.INFURA_API_KEY}`,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

### Step 4: Create .env File
```
INFURA_API_KEY=your_infura_api_key
PRIVATE_KEY=your_metamask_private_key
```

### Step 5: Deploy to Testnet
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

### Step 6: Verify on Etherscan (Optional)
```bash
npx hardhat verify --network sepolia YOUR_CONTRACT_ADDRESS
```

---

## Option 3: Deploy to Polygon Mumbai Testnet

### Step 1: Get MATIC Tokens
- Go to https://faucet.polygon.technology/
- Get free Mumbai MATIC

### Step 2: Configure for Mumbai

Edit `hardhat.config.js`:
```javascript
module.exports = {
  solidity: "0.8.0",
  networks: {
    mumbai: {
      url: "https://rpc-mumbai.maticvigil.com",
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

### Step 3: Deploy
```bash
npx hardhat run scripts/deploy.js --network mumbai
```

---

## Post-Deployment Configuration

### 1. Extract ABI

The deployment script automatically saves the ABI to `backend/contracts/OrderEscrow.json`.

If you need to manually extract it:
```bash
npx hardhat compile
# ABI will be in artifacts/contracts/OrderEscrow.sol/OrderEscrow.json
```

### 2. Update Backend Config

In `backend/config.py`, update:
```python
# Blockchain Configuration
WEB3_PROVIDER_URI = "http://127.0.0.1:8545"  # or Infura URL
SMART_CONTRACT_ADDRESS = "0xYOUR_DEPLOYED_CONTRACT_ADDRESS"
SMART_CONTRACT_ABI_PATH = os.path.join(BASE_DIR, "contracts", "OrderEscrow.json")

# System Wallet (Admin wallet that deploys and manages contract)
SYSTEM_WALLET_ADDRESS = "0xYOUR_ADMIN_WALLET_ADDRESS"
SYSTEM_WALLET_PRIVATE_KEY = "0xYOUR_ADMIN_PRIVATE_KEY"
```

### 3. Test the Integration

Run the test script:
```bash
python test_blockchain_integration.py
```

---

## Troubleshooting

### "Insufficient funds for gas"
- Make sure your wallet has enough ETH/MATIC
- For testnet, use faucets to get free tokens

### "Contract not deployed"
- Check the deployment transaction on Etherscan
- Verify the contract address is correct in config.py

### "Cannot connect to blockchain"
- Verify WEB3_PROVIDER_URI is correct
- For Ganache, make sure it's running on port 8545
- For Infura, check your API key

### "Transaction failed"
- Check gas limits in blockchain_service.py
- Verify wallet has sufficient balance
- Check contract state (order must exist, be in correct state)

---

## Security Notes

⚠️ **IMPORTANT**: 
- Never commit private keys to Git
- Use environment variables for sensitive data
- For production, use a secure key management system
- The system wallet should have limited funds (only for gas)
- Consider using a multi-sig wallet for admin functions

---

## Next Steps

After deployment:
1. Test the complete flow: Payment → Escrow → Delivery → Release
2. Monitor transactions on block explorer
3. Set up event listeners for contract events
4. Implement proper error handling for failed transactions
5. Add transaction retry logic for network issues
