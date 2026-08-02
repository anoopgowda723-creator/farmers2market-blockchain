\# Farmers2Market - System Architecture



\## 1. Overview



Farmers2Market is a blockchain-enabled agricultural marketplace designed to connect farmers directly with buyers while ensuring transparent transactions, secure payments, delivery verification, and trusted order management.



The platform follows a three-tier architecture:



1\. Frontend Layer

2\. Backend API Layer

3\. Database + Blockchain Layer



\## 2. High-Level Architecture



```

&#x20;                        USERS

&#x20;                          |

&#x20;       ---------------------------------------

&#x20;       |                  |                  |

&#x20;     Farmer             Buyer             Admin

&#x20;       |                  |                  |

&#x20;       ---------------------------------------

&#x20;                          |

&#x20;                   Frontend Layer

&#x20;             HTML / CSS / JavaScript

&#x20;             Responsive Web Interface

&#x20;                          |

&#x20;                          |

&#x20;                   REST API Layer

&#x20;                          |

&#x20;                   Flask Backend

&#x20;                          |

&#x20;       ---------------------------------------

&#x20;       |                  |                  |

&#x20;Authentication      Business Logic       Payment

&#x20;  JWT Auth          Order Management    Integration

&#x20;       |                  |                  |

&#x20;       ---------------------------------------

&#x20;                          |

&#x20;                   Data Management Layer

&#x20;                          |

&#x20;       ---------------------------------------

&#x20;       |                                  |

&#x20;  PostgreSQL Database              Blockchain Network

&#x20;       |                                  |

&#x20;User Data                         Ethereum Smart Contract

&#x20;Product Data                      Order Escrow

&#x20;Orders                            Transaction Records

&#x20;Payments                          Verification

```



\# 3. Three Tier Architecture



\## Tier 1: Presentation Layer



The frontend provides user interaction for farmers, buyers, and administrators.



\### Technologies



\* HTML5

\* CSS3

\* JavaScript

\* Bootstrap

\* Responsive UI



\### Responsibilities



\* User registration and login

\* Product browsing

\* Product listing

\* Order placement

\* Order tracking

\* Payment status display

\* Dashboard visualization



```

User

&#x20;|

&#x20;|

Frontend Interface

&#x20;|

&#x20;|

REST API Requests

```



\# Tier 2: Application Layer



The backend handles application logic and communication between frontend, database, and blockchain.



\## Backend Technology



\* Python Flask

\* Flask REST API

\* JWT Authentication

\* SQLAlchemy ORM



\## Backend Components



\### Authentication Module



Responsible for:



\* User registration

\* Login verification

\* JWT token generation

\* Role-based access



Flow:



```

User Login

&#x20;    |

&#x20;    |

Validate Credentials

&#x20;    |

&#x20;    |

Generate JWT Token

&#x20;    |

&#x20;    |

Access Protected APIs

```



\### Farmer Module



Functions:



\* Add agricultural products

\* Update product details

\* Manage inventory

\* View received orders



\### Buyer Module



Functions:



\* Search products

\* Add products to cart

\* Place orders

\* Track delivery



\### Order Management Module



Handles:



\* Order creation

\* Order status updates

\* Blockchain transaction linking



\### Payment Module



Supports:



\* Payment processing

\* Payment verification

\* Transaction recording



\### OTP Service



Used for:



\* User verification

\* Secure authentication



\# 4. Database Architecture



Farmers2Market uses PostgreSQL as the primary database.



\## Database Structure



```

PostgreSQL Database



&#x20;       |

&#x20;       |

&#x20;--------------------------------

&#x20;|              |               |

&#x20;Users       Products        Orders

&#x20;|

&#x20;|

Payments

&#x20;|

&#x20;|

Delivery

&#x20;|

&#x20;|

Audit Logs

```



\## Main Tables



\### Users Table



Stores:



\* User ID

\* Name

\* Email

\* Password Hash

\* Role



\### Products Table



Stores:



\* Product ID

\* Farmer ID

\* Product Name

\* Quantity

\* Price

\* Location



\### Orders Table



Stores:



\* Order ID

\* Buyer ID

\* Product ID

\* Amount

\* Order Status

\* Blockchain Hash



\### Payments Table



Stores:



\* Payment ID

\* Order ID

\* Payment Status

\* Transaction Reference



\# 5. Blockchain Architecture



Farmers2Market uses Ethereum smart contracts for transparent order processing.



\## Smart Contract



Contract:



```

contracts/OrderEscrow.sol

```



\## Blockchain Flow



```

Buyer Places Order

&#x20;         |

&#x20;         |

Create Blockchain Transaction

&#x20;         |

&#x20;         |

Smart Contract Locks Payment

&#x20;         |

&#x20;         |

Farmer Accepts Order

&#x20;         |

&#x20;         |

Delivery Completed

&#x20;         |

&#x20;         |

Payment Released

```



\## Smart Contract Responsibilities



\* Create order escrow

\* Store transaction details

\* Verify order completion

\* Release payment securely



\# 6. Blockchain Deployment Architecture



```

Developer

&#x20;   |

&#x20;   |

Compile Smart Contract

&#x20;   |

&#x20;   |

Deploy Contract

&#x20;   |

&#x20;   |

Ethereum Network / Ganache

&#x20;   |

&#x20;   |

Contract Address

&#x20;   |

&#x20;   |

Flask Backend Integration

```



Deployment Tools:



\* Solidity

\* Hardhat

\* Ganache

\* Web3.py



\# 7. Authentication Architecture



```

User

&#x20;|

&#x20;|

Login Request

&#x20;|

&#x20;|

Flask API

&#x20;|

&#x20;|

Database Verification

&#x20;|

&#x20;|

JWT Token Generated

&#x20;|

&#x20;|

Authorized API Access

```



Security Features:



\* Password hashing

\* JWT authentication

\* Role-based authorization

\* Protected API endpoints



\# 8. Payment Architecture



```

Buyer



&#x20;|

&#x20;|

Payment Gateway



&#x20;|

&#x20;|

Payment Verification



&#x20;|

&#x20;|

Backend API



&#x20;|

&#x20;|

PostgreSQL + Blockchain Record

```



Features:



\* Secure payments

\* Transaction tracking

\* Payment history



\# 9. Delivery Verification Architecture



```

Farmer

&#x20;  |

&#x20;  |

Dispatch Product

&#x20;  |

&#x20;  |

GPS Tracking

&#x20;  |

&#x20;  |

Delivery Verification

&#x20;  |

&#x20;  |

Order Completion

&#x20;  |

&#x20;  |

Blockchain Update

```



Features:



\* Location verification

\* Delivery status updates

\* Transparent tracking



\# 10. Complete System Data Flow



```

&#x20;                Farmer

&#x20;                   |

&#x20;                   |

&#x20;            Add Product

&#x20;                   |

&#x20;                   |

&#x20;             PostgreSQL

&#x20;                   |

&#x20;                   |

Buyer ------------ API ------------ Database

&#x20;|

&#x20;|

Place Order

&#x20;|

&#x20;|

Smart Contract

&#x20;|

&#x20;|

Payment Escrow

&#x20;|

&#x20;|

Delivery Tracking

&#x20;|

&#x20;|

Order Completion

```



\# 11. Security Architecture



Security mechanisms:



\* JWT based authentication

\* Password encryption

\* Environment variables

\* Database access control

\* Smart contract verification



Sensitive information stored in:



```

.env

```



Example:



```

DATABASE\_URL=

JWT\_SECRET\_KEY=

WEB3\_PROVIDER\_URI=

```



\# 12. Deployment Architecture



Production deployment:



```

&#x20;            Users

&#x20;              |

&#x20;              |

&#x20;         Web Browser

&#x20;              |

&#x20;              |

&#x20;         Cloud Server

&#x20;              |

&#x20;      -----------------

&#x20;      |               |

&#x20;   Flask API      PostgreSQL

&#x20;      |

&#x20;      |

&#x20;Ethereum Blockchain

```



Deployment Technologies:



\* AWS EC2

\* PostgreSQL

\* Nginx

\* Gunicorn

\* Ethereum Network



\# 13. Project Directory Structure



```

farmers2market/



│

├── backend/

│   ├── models/

│   ├── routes/

│   ├── services/

│   ├── utils/

│   ├── app.py

│   └── config.py

│

├── contracts/

│   └── OrderEscrow.sol

│

├── scripts/

│   ├── deploy\_contract.py

│   └── test\_contract\_interaction.py

│

├── docs/

│   └── architecture.md

│

├── README.md

│

└── .env

```



\# 14. Architecture Benefits



\## Transparency



Blockchain provides tamper-resistant transaction records.



\## Security



JWT authentication and smart contracts protect user transactions.



\## Scalability



Three-tier architecture allows independent frontend, backend, and database scaling.



\## Reliability



PostgreSQL ensures structured data management while blockchain provides transaction integrity.



\---



\## Farmers2Market Architecture Summary



Farmers2Market combines:



\* Flask REST APIs

\* PostgreSQL database

\* Ethereum smart contracts

\* JWT authentication

\* Payment integration

\* GPS delivery verification



to create a secure and transparent agricultural marketplace connecting farmers and buyers directly.



