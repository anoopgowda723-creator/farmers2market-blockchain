\# Farmers2Market - Blockchain Deployment Guide



\## 1. Blockchain Overview



Farmers2Market integrates Ethereum blockchain technology to provide transparent, secure, and tamper-resistant agricultural transactions.



Blockchain is used for:



\* Secure order escrow

\* Transaction verification

\* Payment transparency

\* Immutable order records

\* Trust between farmers and buyers



\## 2. Blockchain Architecture



```

&#x20;               Buyer



&#x20;                 |



&#x20;                 |



&#x20;           Place Order



&#x20;                 |



&#x20;                 |



&#x20;         Flask Backend API



&#x20;                 |



&#x20;                 |



&#x20;            Web3.py



&#x20;                 |



&#x20;                 |



&#x20;       Ethereum Smart Contract



&#x20;                 |



&#x20;                 |



&#x20;            Blockchain Network



```



\## 3. Blockchain Technologies



| Component           | Technology     |

| ------------------- | -------------- |

| Smart Contract      | Solidity       |

| Blockchain Network  | Ethereum       |

| Development Network | Ganache        |

| Backend Integration | Web3.py        |

| Contract Testing    | Python Scripts |



\## 4. Smart Contract



Location:



```

contracts/OrderEscrow.sol

```



The smart contract manages order escrow between buyers and farmers.



Main responsibilities:



\* Create order

\* Store order information

\* Lock payment

\* Verify completion

\* Release payment



\## 5. Smart Contract Workflow



```

Buyer Creates Order



&#x20;       |



&#x20;       |



Smart Contract Created



&#x20;       |



&#x20;       |



Payment Locked



&#x20;       |



&#x20;       |



Farmer Processes Order



&#x20;       |



&#x20;       |



Delivery Verified



&#x20;       |



&#x20;       |



Payment Released



```



\## 6. Local Blockchain Setup



Farmers2Market uses Ganache for local Ethereum development.



Install Ganache:



Download:



```

https://trufflesuite.com/ganache/

```



Start Ganache:



```

Ganache GUI



or



ganache-cli

```



Default settings:



```

Network:

Ethereum Local





RPC URL:

http://127.0.0.1:7545





Chain ID:

1337

```



\## 7. Install Blockchain Dependencies



Python:



```bash

pip install web3

pip install py-solc-x

```



Node:



```bash

npm install

```



\## 8. Compile Smart Contract



Navigate:



```bash

cd scripts

```



Run:



```bash

python compile\_contract.py

```



Output:



```

Contract compiled successfully



ABI generated



Bytecode generated

```



\## 9. Deploy Smart Contract



Run:



```bash

python deploy\_contract.py

```



Deployment output:



```

Contract deployed successfully



Contract Address:

0xXXXXXXXXXXXX

```



Save contract address in:



```

.env

```



Example:



```env

CONTRACT\_ADDRESS=0xYourContractAddress



WEB3\_PROVIDER\_URI=http://127.0.0.1:7545

```



\## 10. Backend Blockchain Integration



Flask communicates with Ethereum using Web3.py.



Flow:



```

Flask API



&#x20;    |



&#x20;    |



Web3.py Library



&#x20;    |



&#x20;    |



Ethereum Smart Contract



&#x20;    |



&#x20;    |



Transaction Receipt



```



\## 11. Blockchain Order Creation



Example:



```python

transaction = contract.functions.createOrder(

&#x20;   order\_id,

&#x20;   amount

).transact()

```



After successful transaction:



```

Transaction Hash Generated



&#x20;       |



Stored in PostgreSQL



&#x20;       |



Visible on Blockchain



```



\## 12. Testing Blockchain Connection



Run:



```bash

python scripts/test\_blockchain\_connection.py

```



Expected output:



```

Connected to Ethereum Network



Chain ID: 1337



Blockchain Status: Active

```



\## 13. Testing Smart Contract



Run:



```bash

python scripts/test\_contract\_interaction.py

```



Expected:



```

Contract Interaction Successful



Order Created Successfully

```



\## 14. Production Blockchain Architecture



```

&#x20;                Users



&#x20;                  |



&#x20;                  |



&#x20;             Flask Backend



&#x20;                  |



&#x20;                  |



&#x20;                Web3.py



&#x20;                  |



&#x20;                  |



&#x20;         Ethereum Mainnet/Testnet



&#x20;                  |



&#x20;                  |



&#x20;           Smart Contract



```



\## 15. Security Considerations



Implemented security:



\* Smart contract validation

\* Transaction verification

\* Secure private keys

\* Environment variable storage

\* Backend authorization



Never store:



```

Private Keys



API Secrets



Passwords

```



inside source code.



\## 16. Blockchain Benefits



\### Transparency



Every transaction can be verified.



\### Security



Blockchain records cannot be modified.



\### Trust



Farmers and buyers can interact without intermediaries.



\### Payment Protection



Escrow prevents payment fraud.



\---



\# Farmers2Market Blockchain Summary



Farmers2Market combines Flask APIs, PostgreSQL, and Ethereum smart contracts to create a secure blockchain-powered agricultural marketplace.



Blockchain provides:



\* Transparent orders

\* Secure payments

\* Verified transactions

\* Trusted farmer-buyer relationships



```

```



