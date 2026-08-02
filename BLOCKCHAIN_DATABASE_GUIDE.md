# Blockchain Database Information Guide

## 📊 Database Table: `blockchain_orders`

Your blockchain-related information is stored in the **`blockchain_orders`** table in your MySQL database.

---

## 🗂️ Table Structure

### Table Name
```
blockchain_orders
```

### Columns

| Column | Type | Description |
|--------|------|-------------|
| **id** | BigInteger | Primary key |
| **order_id** | BigInteger | Foreign key to `orders.id` (unique, one blockchain record per order) |
| **onchain_order_id** | String(191) | Order ID as stored on the blockchain |
| **tx_hash_create** | String(191) | Transaction hash when order was created on blockchain |
| **tx_hash_release** | String(191) | Transaction hash when funds were released to farmer |
| **tx_hash_refund** | String(191) | Transaction hash if order was refunded |
| **state** | Enum | Current blockchain state (see states below) |
| **created_at** | DateTime | When blockchain record was created |
| **updated_at** | DateTime | Last update timestamp |

---

## 📋 Blockchain States

The `state` column can have these values:

1. **CREATED** - Order created but not yet paid
2. **PAID** - Payment received, funds in escrow
3. **FARMER_CONFIRMED** - Farmer confirmed the order
4. **OUT_FOR_DELIVERY** - Order is being delivered
5. **DELIVERED** - Delivery completed with proof
6. **FUNDS_RELEASED** - Funds released to farmer
7. **REFUNDED** - Order refunded to buyer

---

## 🔍 How to Query Blockchain Data

### Using MySQL Workbench or Command Line

#### 1. View All Blockchain Orders
```sql
SELECT * FROM blockchain_orders;
```

#### 2. View Blockchain Info for a Specific Order
```sql
SELECT 
    bo.*,
    o.id as order_number,
    o.total_amount,
    o.status as order_status
FROM blockchain_orders bo
JOIN orders o ON bo.order_id = o.id
WHERE o.id = 123;  -- Replace with your order ID
```

#### 3. View All Orders with Transaction Hashes
```sql
SELECT 
    o.id,
    o.total_amount,
    bo.state as blockchain_state,
    bo.tx_hash_create,
    bo.tx_hash_release,
    bo.created_at
FROM orders o
LEFT JOIN blockchain_orders bo ON o.id = bo.order_id
WHERE bo.id IS NOT NULL
ORDER BY o.created_at DESC;
```

#### 4. View Orders by Blockchain State
```sql
SELECT 
    o.id,
    u.name as buyer_name,
    o.total_amount,
    bo.state,
    bo.tx_hash_create
FROM blockchain_orders bo
JOIN orders o ON bo.order_id = o.id
JOIN users u ON o.user_id = u.id
WHERE bo.state = 'PAID'  -- or any other state
ORDER BY bo.created_at DESC;
```

#### 5. Track Fund Releases
```sql
SELECT 
    o.id,
    o.total_amount,
    bo.tx_hash_release,
    bo.updated_at as released_at
FROM blockchain_orders bo
JOIN orders o ON bo.order_id = o.id
WHERE bo.state = 'FUNDS_RELEASED'
ORDER BY bo.updated_at DESC;
```

---

## 🔗 Relationship with Orders Table

Each order in the `orders` table can have **one** corresponding record in `blockchain_orders`:

```
orders (1) ←→ (1) blockchain_orders
```

- **order_id** in `blockchain_orders` references **id** in `orders`
- This is a **one-to-one** relationship
- Not all orders have blockchain records (only online payments)

---

## 💻 Using Python/Flask to Query

### Example 1: Get Blockchain Info for an Order
```python
from models.blockchain_order import BlockchainOrder
from models.order import Order

# Get order with blockchain info
order = Order.query.get(123)
if order.blockchain_order:
    print(f"Blockchain State: {order.blockchain_order.state}")
    print(f"Create TX: {order.blockchain_order.tx_hash_create}")
    print(f"Release TX: {order.blockchain_order.tx_hash_release}")
```

### Example 2: Get All Paid Orders on Blockchain
```python
from models.blockchain_order import BlockchainOrder

paid_orders = BlockchainOrder.query.filter_by(state='PAID').all()
for bo in paid_orders:
    print(f"Order {bo.order_id}: {bo.state}")
    print(f"TX Hash: {bo.tx_hash_create}")
```

### Example 3: Track Transaction Hashes
```python
from models.blockchain_order import BlockchainOrder

# Get all orders with transaction hashes
orders_with_tx = BlockchainOrder.query.filter(
    BlockchainOrder.tx_hash_create.isnot(None)
).all()

for bo in orders_with_tx:
    print(f"Order: {bo.order_id}")
    print(f"Create TX: {bo.tx_hash_create}")
    if bo.tx_hash_release:
        print(f"Release TX: {bo.tx_hash_release}")
```

---

## 🔎 Viewing in Ganache

You can also view blockchain transactions directly in Ganache:

1. **Ganache Terminal** - Shows all transactions in real-time
2. **Transaction Hashes** - Copy from database and search on blockchain explorer
3. **Contract Events** - View events emitted by smart contract

### Verify Transaction on Ganache
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Get transaction from database
tx_hash = "0x..."  # From blockchain_orders.tx_hash_create

# Get transaction details
tx = w3.eth.get_transaction(tx_hash)
receipt = w3.eth.get_transaction_receipt(tx_hash)

print(f"Block Number: {receipt.blockNumber}")
print(f"Gas Used: {receipt.gasUsed}")
print(f"Status: {'Success' if receipt.status == 1 else 'Failed'}")
```

---

## 📊 Database Access Methods

### Method 1: MySQL Workbench
1. Open MySQL Workbench
2. Connect to your database: `farmer_market_db`
3. Navigate to Tables → `blockchain_orders`
4. Right-click → "Select Rows - Limit 1000"

### Method 2: Command Line
```bash
mysql -u root -p
USE farmer_market_db;
SELECT * FROM blockchain_orders;
```

### Method 3: Python Script
```python
# Create a script: check_blockchain_orders.py
from backend.extensions import db
from backend.models.blockchain_order import BlockchainOrder
from backend.app import create_app

app = create_app()
with app.app_context():
    orders = BlockchainOrder.query.all()
    for order in orders:
        print(f"Order {order.order_id}: {order.state}")
        print(f"  Create TX: {order.tx_hash_create}")
        print(f"  Release TX: {order.tx_hash_release}")
        print()
```

### Method 4: Flask Shell
```bash
cd backend
flask shell

>>> from models.blockchain_order import BlockchainOrder
>>> BlockchainOrder.query.all()
>>> # Query and inspect blockchain orders
```

---

## 🎯 Common Queries

### Find Orders Stuck in Escrow
```sql
SELECT 
    o.id,
    o.total_amount,
    bo.state,
    bo.created_at,
    TIMESTAMPDIFF(HOUR, bo.created_at, NOW()) as hours_in_escrow
FROM blockchain_orders bo
JOIN orders o ON bo.order_id = o.id
WHERE bo.state IN ('PAID', 'FARMER_CONFIRMED', 'OUT_FOR_DELIVERY')
ORDER BY bo.created_at ASC;
```

### Calculate Total Funds in Escrow
```sql
SELECT 
    COUNT(*) as orders_in_escrow,
    SUM(o.total_amount) as total_amount_in_escrow
FROM blockchain_orders bo
JOIN orders o ON bo.order_id = o.id
WHERE bo.state NOT IN ('FUNDS_RELEASED', 'REFUNDED');
```

### Audit Trail of All Transactions
```sql
SELECT 
    o.id,
    u.name as buyer,
    o.total_amount,
    bo.state,
    bo.tx_hash_create as create_transaction,
    bo.tx_hash_release as release_transaction,
    bo.created_at,
    bo.updated_at
FROM blockchain_orders bo
JOIN orders o ON bo.order_id = o.id
JOIN users u ON o.user_id = u.id
ORDER BY bo.created_at DESC;
```

---

## 🔐 Important Notes

1. **Transaction Hashes** are stored as strings (66 characters including '0x')
2. **State transitions** are tracked automatically by the backend
3. **One-to-one relationship** with orders table
4. **Only online payments** create blockchain records
5. **COD orders** do NOT have blockchain records

---

## 📍 Database Location

**Database:** `farmer_market_db`  
**Table:** `blockchain_orders`  
**Host:** `localhost`  
**User:** `root`  
**Connection String:** `mysql+pymysql://root:Rahul%402003@localhost/farmer_market_db`

---

## 🚀 Quick Access Commands

```bash
# View blockchain orders in database
mysql -u root -p -e "USE farmer_market_db; SELECT * FROM blockchain_orders;"

# Count blockchain orders by state
mysql -u root -p -e "USE farmer_market_db; SELECT state, COUNT(*) FROM blockchain_orders GROUP BY state;"

# View recent blockchain transactions
mysql -u root -p -e "USE farmer_market_db; SELECT order_id, state, tx_hash_create, created_at FROM blockchain_orders ORDER BY created_at DESC LIMIT 10;"
```

---

## 📚 Related Files

- **Model:** [`backend/models/blockchain_order.py`](file:///c:/farmer_market/backend/models/blockchain_order.py)
- **Service:** [`backend/services/blockchain_service.py`](file:///c:/farmer_market/backend/services/blockchain_service.py)
- **Smart Contract:** [`contracts/OrderEscrow.sol`](file:///c:/farmer_market/contracts/OrderEscrow.sol)

---

**Need to query blockchain data? Use the SQL examples above or access via Python/Flask!** 🎉
