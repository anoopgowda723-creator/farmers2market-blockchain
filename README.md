\# 🌱 Farmers2Market - Blockchain Enabled Agricultural Marketplace



A decentralized agricultural marketplace that connects farmers directly with buyers using blockchain technology, secure REST APIs, GPS-based delivery verification, and hybrid payment processing.



Farmers2Market improves transparency in agricultural supply chains by reducing intermediaries and providing secure digital transactions between farmers and buyers.



\---



\## 📌 Project Overview



Farmers2Market is a full-stack blockchain-based agriculture marketplace designed to digitize the farming supply chain.



The platform allows:



\- Farmers to sell agricultural products directly to buyers

\- Buyers to purchase products securely

\- Smart contracts to provide transparent transactions

\- Delivery partners to verify deliveries using GPS tracking

\- Secure payments through hybrid payment processing



The system follows a three-tier architecture:



```

Frontend

&#x20;   |

Backend REST API

&#x20;   |

Database + Blockchain Layer

```



\---



\# 🚀 Key Features



\## 👨‍🌾 Farmer Module



\- Farmer registration and authentication

\- Add and manage agricultural products

\- Update product details

\- View customer orders

\- Track payments and settlements





\## 🛒 Buyer Module



\- Browse agricultural products

\- Search products

\- Add products to cart

\- Place orders

\- Track order status

\- View transaction history





\## 🚚 Delivery Module



\- Delivery partner management

\- GPS-based delivery verification

\- Delivery status updates

\- Order tracking





\## 🔐 Security Features



\- JWT authentication

\- Role-based access control

\- Password hashing

\- Secure API endpoints

\- Environment-based configuration





\## ⛓️ Blockchain Features



\- Ethereum smart contract integration

\- Blockchain-based order verification

\- Transparent transaction records

\- Escrow-based payment mechanism

\- Web3 blockchain communication





\## 💳 Payment Features



\- Hybrid payment processing

\- Razorpay integration

\- Payment verification

\- Transaction history management





\---



\# 🏗️ System Architecture



```

&#x20;                   Users



&#x20;     Farmer        Buyer        Delivery Partner

&#x20;         \\          |              /

&#x20;          \\         |             /

&#x20;               Frontend



&#x20;                   |

&#x20;                   |



&#x20;            Flask REST API



&#x20;                   |

&#x20;    --------------------------------

&#x20;    |              |               |

&#x20;PostgreSQL     JWT Auth      Blockchain



&#x20;                   |

&#x20;             Ethereum Network



&#x20;                   |

&#x20;            Smart Contract

```



\---



\# 🛠️ Technology Stack



\## Backend



\- Python

\- Flask

\- Flask REST API

\- SQLAlchemy

\- JWT Authentication





\## Database



\- PostgreSQL





\## Blockchain



\- Ethereum

\- Solidity

\- Web3.py

\- Ganache





\## Frontend



\- HTML5

\- CSS3

\- JavaScript

\- Bootstrap





\## Payment



\- Razorpay API





\## Cloud \& Tools



\- AWS EC2

\- Docker

\- Git

\- GitHub

\- Postman

\- VS Code





\---



\# 📂 Project Structure



```

farmers2market-blockchain/



│

├── backend/

│   ├── app.py

│   ├── config.py

│   ├── models/

│   ├── routes/

│   ├── services/

│   └── utils/

│

├── contracts/

│   └── OrderEscrow.sol

│

├── scripts/

│   ├── compile\_contract.py

│   ├── deploy\_contract.py

│   ├── test\_blockchain\_connection.py

│   └── test\_contract\_interaction.py

│

├── requirements.txt

├── .env.example

└── README.md

```



\---



\# ⚙️ Installation Guide



\## Clone Repository



```bash

git clone https://github.com/anoopgowda723-creator/farmers2market-blockchain.git



cd farmers2market-blockchain

```



\---



\# Backend Setup



Create virtual environment:



```bash

python -m venv venv

```



Activate environment:



Windows:



```bash

venv\\Scripts\\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\---



\# 🗄️ PostgreSQL Database Setup



Create database:



```sql

CREATE DATABASE farmer2market;

```



Configure `.env` file:



```env

DB\_HOST=localhost

DB\_PORT=5432

DB\_NAME=farmer2market

DB\_USER=postgres

DB\_PASSWORD=your\_password



DATABASE\_URL=postgresql://postgres:your\_password@localhost:5432/farmer2market

```



\---



\# ⛓️ Blockchain Setup



Start Ganache:



```bash

ganache

```



Compile smart contract:



```bash

python scripts/compile\_contract.py

```



Deploy smart contract:



```bash

python scripts/deploy\_contract.py

```



Test blockchain connection:



```bash

python scripts/test\_blockchain\_connection.py

```



\---



\# ▶️ Run Application



Start Flask backend:



```bash

python backend/app.py

```



Application:



```

http://localhost:5000

```



\---



\# 🔑 API Modules



\## Authentication



\- Register User

\- Login

\- JWT Token Generation





\## Farmer APIs



\- Product Management

\- Order Management

\- Settlement Tracking





\## Buyer APIs



\- Product Browsing

\- Cart Management

\- Order Placement





\## Payment APIs



\- Payment Processing

\- Transaction Verification





\---



\# 📊 Database Models



Main database entities:



```

User



Product



Order



Payment



Settlement



Delivery



Blockchain Order



Audit Log



Notification

```



\---



\# 🌟 Advantages



✅ Direct farmer-to-buyer marketplace  

✅ Blockchain transaction transparency  

✅ Secure authentication  

✅ Digital payment integration  

✅ GPS delivery verification  

✅ Improved agricultural supply chain  





\---



\# 🔮 Future Enhancements



\- AI-based crop price prediction

\- IoT farm monitoring

\- Mobile application

\- AI demand forecasting

\- Multi-chain blockchain support





\---



\# 👨‍💻 Developer



\## Anoop BP



Full Stack Developer | Blockchain Developer



GitHub:

https://github.com/anoopgowda723-creator



LinkedIn:

https://www.linkedin.com/in/anoop-b-p-8276a4392



Portfolio:

https://developer-portfolio-eight-tau.vercel.app





\---



\# 📜 License



Developed for educational and research purposes.

