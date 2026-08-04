<div align="center">

# 🌱 Farmers2Market
### Blockchain Enabled Agricultural Marketplace

A decentralized agricultural marketplace connecting **Farmers**, **Buyers**, and **Delivery Partners** using **Blockchain Technology**, **Ethereum Smart Contracts**, **Flask REST APIs**, **PostgreSQL**, **JWT Authentication**, **GPS Delivery Verification**, and **Hybrid Payment Processing**.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-REST%20API-black?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Ethereum](https://img.shields.io/badge/Ethereum-Blockchain-627EEA?style=for-the-badge&logo=ethereum)
![Solidity](https://img.shields.io/badge/Solidity-Smart%20Contracts-363636?style=for-the-badge&logo=solidity)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge)
![Razorpay](https://img.shields.io/badge/Razorpay-Payment-blue?style=for-the-badge)
![AWS](https://img.shields.io/badge/AWS-EC2-orange?style=for-the-badge&logo=amazonaws)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

# 📖 Table of Contents

- Project Overview
- Key Features
- System Architecture
- Technology Stack
- Project Screenshots
- Folder Structure
- Installation Guide
- Configuration
- Database Setup
- Blockchain Setup
- Running the Application
- REST API Documentation
- Database Design
- Smart Contract Workflow
- Security Features
- Testing
- Deployment
- Future Enhancements
- Contributing
- License
- Developer

---

# 🌾 Project Overview

Farmers2Market is a full-stack blockchain-powered agricultural marketplace designed to eliminate intermediaries between farmers and buyers.

The platform enables secure and transparent transactions through Ethereum smart contracts while providing modern REST APIs for seamless communication between users and the backend.

Unlike traditional agricultural marketplaces, Farmers2Market ensures transparency, secure digital payments, verified deliveries, and immutable transaction records using blockchain technology.

The project demonstrates practical implementation of:

- Blockchain Integration
- Smart Contracts
- REST API Development
- PostgreSQL Database Design
- Authentication & Authorization
- Payment Gateway Integration
- GPS-based Delivery Verification
- Cloud Deployment

---

# 🎯 Objectives

The primary objectives of this project are:

- Connect farmers directly with buyers
- Remove unnecessary intermediaries
- Increase transparency using blockchain
- Enable secure online payments
- Track product deliveries
- Maintain immutable transaction history
- Build a scalable REST API backend
- Demonstrate blockchain adoption in agriculture

---

# ✨ Key Features

## 👨‍🌾 Farmer Module

- Farmer Registration
- Secure Login using JWT
- Product Management
- Inventory Management
- Order Tracking
- Payment History
- Settlement Reports

---

## 🛒 Buyer Module

- User Registration
- Browse Products
- Product Search
- Shopping Cart
- Order Placement
- Payment Processing
- Order History

---

## 🚚 Delivery Module

- Delivery Assignment
- GPS Verification
- Delivery Status Updates
- Live Order Tracking
- Delivery Confirmation

---

## 🔐 Authentication & Security

- JWT Authentication
- Password Hashing
- Role-Based Access Control
- Protected REST APIs
- Secure Environment Variables
- SQL Injection Protection
- Authentication Middleware

---

## ⛓ Blockchain Features

- Ethereum Smart Contracts
- Transparent Transactions
- Immutable Records
- Escrow Payment Mechanism
- Blockchain Order Verification
- Web3.py Integration
- Ganache Development Network

---

## 💳 Payment Features

- Razorpay Integration
- Secure Payment Verification
- Transaction History
- Hybrid Payment Processing
- Payment Status Tracking

---

# 🏗 System Architecture

```text
                        Users
     ______________________________________________

       Farmer      Buyer      Delivery Partner

                  Frontend (HTML/CSS/JS)

                         │

                 Flask REST API Server

                         │

        ┌────────────┬───────────────┬─────────────┐
        │            │               │
   PostgreSQL     JWT Auth      Blockchain Layer
        │                            │
        │                     Ethereum Network
        │                            │
        └────────────── Smart Contract ───────────
```

---

# 🌍 Workflow

```text
Farmer

↓

Upload Products

↓

Buyer Browses Products

↓

Buyer Places Order

↓

Payment Initiated

↓

Smart Contract Verification

↓

Order Stored in PostgreSQL

↓

Delivery Partner Assigned

↓

GPS Delivery Verification

↓

Payment Released

↓

Transaction Recorded on Blockchain
```

---

# 📸 Application Screenshots

> Store all screenshots inside the `/screenshots` folder.

## Home Page

![Home](screenshots/home.png)

---

## User Registration

![Register](screenshots/register.png)

---

## User Login

![Login](screenshots/login.png)

---

## Farmer Dashboard

![Dashboard](screenshots/dashboard.png)

---


## Order Management

![Orders](screenshots/orders.png)

---

## Payment Gateway

![Payment](screenshots/payment.png)

---

## Blockchain Transaction

![Blockchain](screenshots/blockchain.png)

---

# 📊 Project Statistics

| Feature | Status |
|----------|--------|
| Blockchain Integration | ✅ |
| PostgreSQL Database | ✅ |
| Flask REST APIs | ✅ |
| JWT Authentication | ✅ |
| Ethereum Smart Contracts | ✅ |
| GPS Delivery Tracking | ✅ |
| Razorpay Payments | ✅ |
| Responsive UI | ✅ |
| Cloud Deployment Ready | ✅ |

---

# ⭐ Why This Project?

This project demonstrates modern software engineering practices by combining backend development, blockchain technology, database management, secure authentication, payment gateway integration, and cloud deployment into a real-world agricultural marketplace.

It showcases practical experience in building scalable, secure, and production-ready web applications while addressing real-world supply chain challenges.

---
# 🛠 Technology Stack

## Backend

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Backend Programming |
| Flask | Web Framework |
| Flask-RESTful | REST API Development |
| SQLAlchemy | ORM |
| Flask-JWT-Extended | JWT Authentication |
| Flask-Migrate | Database Migration |
| Flask-CORS | Cross-Origin Resource Sharing |
| Werkzeug | Password Hashing |

---

## Frontend

| Technology | Purpose |
|------------|---------|
| HTML5 | Page Structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Client-side Logic |

---

## Database

| Technology | Purpose |
|------------|---------|
| PostgreSQL | Relational Database |
| SQLAlchemy ORM | Database Operations |

---

## Blockchain

| Technology | Purpose |
|------------|---------|
| Ethereum | Blockchain Network |
| Solidity | Smart Contracts |
| Web3.py | Blockchain Communication |
| Ganache | Local Blockchain |

---

## Payment Gateway

- Razorpay Payment Integration
- Payment Verification
- Secure Transactions

---

## Cloud & DevOps

- AWS EC2
- Docker
- Git
- GitHub
- Postman
- VS Code

---

# 📂 Project Structure

```text
farmers2market-blockchain/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── middleware/
│   ├── utils/
│   ├── static/
│   └── templates/
│
├── contracts/
│   ├── FarmerMarketplace.sol
│   └── OrderEscrow.sol
│
├── scripts/
│   ├── compile_contract.py
│   ├── deploy_contract.py
│   ├── migrate_database.py
│   └── blockchain_tests.py
│
├── screenshots/
│
├── docs/
│
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── README.md
└── LICENSE
```

---

# ⚙ Prerequisites

Install the following software before running the project.

- Python 3.11+
- PostgreSQL 16+
- Ganache
- Node.js (optional)
- Git
- MetaMask Browser Extension

---

# 🚀 Installation Guide

## Clone Repository

```bash
git clone https://github.com/anoopgowda723-creator/farmers2market-blockchain.git
```

```bash
cd farmers2market-blockchain
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Linux / macOS

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

Verify installation

```bash
pip list
```

---

# 🔧 Environment Variables

Create a file named

```
.env
```

Copy the following configuration.

```env
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

DATABASE_URL=postgresql://postgres:password@localhost:5432/farmer2market

DB_HOST=localhost

DB_PORT=5432

DB_NAME=farmer2market

DB_USER=postgres

DB_PASSWORD=your_password

ETH_NODE_URL=http://127.0.0.1:7545

SMART_CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS

PRIVATE_KEY=YOUR_PRIVATE_KEY

RAZORPAY_KEY_ID=YOUR_KEY

RAZORPAY_KEY_SECRET=YOUR_SECRET
```

---

# 🗄 PostgreSQL Database Setup

Start PostgreSQL server.

Create database

```sql
CREATE DATABASE farmer2market;
```

Connect

```sql
\c farmer2market;
```

Run migrations

```bash
flask db init
```

```bash
flask db migrate
```

```bash
flask db upgrade
```

---

# ⛓ Blockchain Setup

## Start Ganache

Launch Ganache Desktop.

Default RPC URL

```
http://127.0.0.1:7545
```

---

## Compile Smart Contract

```bash
python scripts/compile_contract.py
```

---

## Deploy Smart Contract

```bash
python scripts/deploy_contract.py
```

Example Output

```
Contract deployed successfully.

Contract Address:

0xXXXXXXXXXXXXXXX
```

Copy the generated contract address into

```
.env
```

---

# 💳 Razorpay Configuration

Create Razorpay account.

Generate

- Key ID
- Secret Key

Update

```
.env
```

```
RAZORPAY_KEY_ID=xxxxxxxx

RAZORPAY_KEY_SECRET=xxxxxxxx
```

---

# ▶ Running the Application

Start Flask server

```bash
python backend/app.py
```

or

```bash
flask run
```

Application URL

```
http://127.0.0.1:5000
```

---

# 📡 API Base URL

```
http://127.0.0.1:5000/api/
```

---

# 🔍 Verify Installation

Open browser

```
http://127.0.0.1:5000
```

Expected Result

- Login Page
- Register Page
- PostgreSQL Connected
- Blockchain Connected
- JWT Authentication Enabled

---

# 🐳 Docker (Optional)

Build

```bash
docker build -t farmers2market .
```

Run

```bash
docker run -p 5000:5000 farmers2market
```

Using Docker Compose

```bash
docker-compose up --build
```

---

# ✅ Installation Complete

You are now ready to use the Farmers2Market Blockchain Marketplace.

The next section covers:

- 📘 Complete REST API Documentation
- 🔐 Authentication APIs
- 👨‍🌾 Farmer APIs
- 🛒 Buyer APIs
- 🚚 Delivery APIs
- 💳 Payment APIs
- ⛓ Blockchain APIs
- 📊 Database Models
- Entity Relationship Diagram

# 📘 REST API Documentation

## Base URL

```
http://127.0.0.1:5000/api
```

---

# 🔐 Authentication APIs

## Register User

| Method | Endpoint |
|---------|----------|
| POST | `/auth/register` |

### Request

```json
{
    "name":"Anoop",
    "email":"anoop@gmail.com",
    "password":"password123",
    "role":"farmer"
}
```

### Response

```json
{
    "message":"User registered successfully."
}
```

---

## Login

| Method | Endpoint |
|---------|----------|
| POST | `/auth/login` |

### Request

```json
{
    "email":"anoop@gmail.com",
    "password":"password123"
}
```

### Response

```json
{
    "access_token":"JWT_TOKEN"
}
```

---

## Get Profile

| Method | Endpoint |
|---------|----------|
| GET | `/auth/profile` |

Authentication Required

```
Bearer Token
```

---

# 👨‍🌾 Farmer APIs

## Add Product

| Method | Endpoint |
|---------|----------|
| POST | `/products` |

---

## View Products

| Method | Endpoint |
|---------|----------|
| GET | `/products` |

---

## Update Product

| Method | Endpoint |
|---------|----------|
| PUT | `/products/<id>` |

---

## Delete Product

| Method | Endpoint |
|---------|----------|
| DELETE | `/products/<id>` |

---

## View Orders

| Method | Endpoint |
|---------|----------|
| GET | `/farmer/orders` |

---

## Settlement History

| Method | Endpoint |
|---------|----------|
| GET | `/farmer/settlements` |

---

# 🛒 Buyer APIs

## Browse Products

| Method | Endpoint |
|---------|----------|
| GET | `/products` |

---

## Search Products

| Method | Endpoint |
|---------|----------|
| GET | `/products/search?q=` |

---

## Add to Cart

| Method | Endpoint |
|---------|----------|
| POST | `/cart` |

---

## View Cart

| Method | Endpoint |
|---------|----------|
| GET | `/cart` |

---

## Place Order

| Method | Endpoint |
|---------|----------|
| POST | `/orders` |

---

## Order History

| Method | Endpoint |
|---------|----------|
| GET | `/orders/history` |

---

# 🚚 Delivery APIs

## Assigned Orders

| Method | Endpoint |
|---------|----------|
| GET | `/delivery/orders` |

---

## Update Delivery Status

| Method | Endpoint |
|---------|----------|
| PUT | `/delivery/status/<id>` |

---

## GPS Verification

| Method | Endpoint |
|---------|----------|
| POST | `/delivery/gps` |

---

# 💳 Payment APIs

## Create Payment

| Method | Endpoint |
|---------|----------|
| POST | `/payment/create` |

---

## Verify Payment

| Method | Endpoint |
|---------|----------|
| POST | `/payment/verify` |

---

## Payment History

| Method | Endpoint |
|---------|----------|
| GET | `/payment/history` |

---

# ⛓ Blockchain APIs

## Deploy Smart Contract

| Method | Endpoint |
|---------|----------|
| POST | `/blockchain/deploy` |

---

## Verify Blockchain Transaction

| Method | Endpoint |
|---------|----------|
| GET | `/blockchain/verify/<transaction_hash>` |

---

## Transaction History

| Method | Endpoint |
|---------|----------|
| GET | `/blockchain/history` |

---

# 🗃 Database Models

## User

```text
id
name
email
password
role
created_at
```

---

## Product

```text
id
farmer_id
product_name
category
quantity
price
image
created_at
```

---

## Order

```text
id
buyer_id
product_id
quantity
status
created_at
```

---

## Payment

```text
id
order_id
payment_id
amount
status
created_at
```

---

## Delivery

```text
id
order_id
driver_id
latitude
longitude
status
```

---

## BlockchainOrder

```text
id
order_id
contract_address
transaction_hash
block_number
```

---

# 🧩 Entity Relationship Diagram

```text
User
 │
 ├───────────────┐
 │               │
Product       Delivery
 │               │
 │               │
Order────────────┘
 │
 │
Payment
 │
 │
BlockchainOrder
```

---

# 🔐 Security Features

✔ JWT Authentication

✔ Password Hashing

✔ Role-Based Authorization

✔ Protected REST APIs

✔ Secure Environment Variables

✔ PostgreSQL ORM Protection

✔ Smart Contract Validation

✔ Secure Payment Verification

✔ CORS Protection

---

# ⛓ Blockchain Workflow

```text
Farmer

↓

Uploads Product

↓

Buyer Places Order

↓

Payment Initiated

↓

Smart Contract Triggered

↓

Ethereum Blockchain

↓

Transaction Hash Generated

↓

Stored in PostgreSQL

↓

Delivery Assigned

↓

GPS Verification

↓

Payment Released

↓

Order Completed
```

---

# 💳 Payment Workflow

```text
Buyer

↓

Checkout

↓

Razorpay Payment

↓

Payment Verification

↓

Blockchain Verification

↓

Database Update

↓

Order Confirmation
```

---

# 📈 Application Flow

```text
Register

↓

Login

↓

JWT Token Generated

↓

Browse Products

↓

Place Order

↓

Payment

↓

Blockchain Verification

↓

Delivery

↓

GPS Verification

↓

Order Completed
```

---

# 🧪 Testing

## Unit Tests

```bash
pytest
```

## API Testing

Use **Postman** to test all REST endpoints.

## Blockchain Testing

```bash
python scripts/test_blockchain_connection.py
```

## Database Testing

```bash
python check_db.py
```

---

# 📊 Performance Highlights

- RESTful API Architecture
- JWT-secured Authentication
- PostgreSQL Relational Database
- Ethereum Smart Contracts
- GPS Delivery Verification
- Hybrid Payment Processing
- Scalable Modular Backend
- Cloud Deployment Ready

---

# 📚 Documentation

Additional documentation is available in the **docs/** directory:

- Deployment Guide
- Blockchain Database Guide
- Ganache Setup Guide
- Quick Start Guide
- Setup Steps
- Project Presentation
- Viva Notes
- Architecture Documentation

---

✅ **Part 3 Complete**

**Part 4** will include:
- 🚀 AWS EC2 Deployment
- 🤝 Contributing Guide
- 🛣️ Roadmap
- ❓FAQ
- 📝 Changelog
- 📄 MIT License
- 👨‍💻 Developer Profile
- 📬 Contact Information
- 🌟 Support the Project
- 🙏 Acknowledgements
- ❤️ Final Professional Footer

# 🚀 Deployment

## AWS EC2 Deployment

### Launch an EC2 Instance

- Ubuntu 22.04 LTS
- t2.micro (Free Tier)
- Open ports:
  - 22 (SSH)
  - 80 (HTTP)
  - 443 (HTTPS)
  - 5000 (Flask - Development)

---

### Clone Repository

```bash
git clone https://github.com/anoopgowda723-creator/farmers2market-blockchain.git
```

```bash
cd farmers2market-blockchain
```

---

### Install Dependencies

```bash
sudo apt update
```

```bash
sudo apt install python3-pip python3-venv postgresql git -y
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create

```
.env
```

Update

```
DATABASE_URL

JWT_SECRET_KEY

SECRET_KEY

ETH_NODE_URL

SMART_CONTRACT_ADDRESS

RAZORPAY_KEY_ID

RAZORPAY_KEY_SECRET
```

---

### Start Application

```bash
python backend/app.py
```

---

# 📈 Project Roadmap

## ✅ Completed

- JWT Authentication
- Farmer Module
- Buyer Module
- Product Management
- PostgreSQL Integration
- Ethereum Smart Contracts
- GPS Delivery Tracking
- Razorpay Payment Gateway
- REST APIs

---

## 🚧 In Progress

- Docker Deployment
- Admin Dashboard
- Email Notifications
- SMS Notifications

---

## 🔮 Future Scope

- AI Crop Price Prediction
- Machine Learning Recommendations
- Mobile Application
- IoT Sensor Integration
- Live Vehicle Tracking
- QR Code Verification
- Multi-language Support
- Kubernetes Deployment
- CI/CD Pipeline
- Analytics Dashboard

---

# 🤝 Contributing

Contributions are welcome.

### Steps

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature/NewFeature
```

3. Commit changes

```bash
git commit -m "Add new feature"
```

4. Push

```bash
git push origin feature/NewFeature
```

5. Open a Pull Request

---

# 📋 Coding Standards

- Follow PEP 8
- Use meaningful variable names
- Write modular code
- Add comments where required
- Validate user inputs
- Keep API responses consistent

---

# 🧪 Testing

Run all tests

```bash
pytest
```

Test blockchain

```bash
python scripts/test_blockchain_connection.py
```

Test database

```bash
python check_db.py
```

---

# ❓ Frequently Asked Questions

### Which database is used?

PostgreSQL

---

### Which blockchain is used?

Ethereum

---

### Which framework is used?

Flask REST API

---

### Which authentication method is used?

JWT Authentication

---

### Which payment gateway is used?

Razorpay

---

### Can this project be deployed?

Yes.

It can be deployed on:

- AWS EC2
- Docker
- Render
- Railway
- Azure
- DigitalOcean

---

# 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Anoop BP

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software
and associated documentation files (the "Software"),
to deal in the Software without restriction.
```

---

# 👨‍💻 Developer

## Anoop BP

**Full Stack Developer | Backend Developer | Blockchain Enthusiast**

### 📧 Email

anoopgowda723@gmail.com

### 💼 LinkedIn

https://www.linkedin.com/in/anoop-b-p-8276a4392

### 💻 GitHub

https://github.com/anoopgowda723-creator

### 🌐 Portfolio

https://developer-portfolio-eight-tau.vercel.app

---

# 🏆 Project Highlights

- Full Stack Web Application
- Blockchain Integration
- Ethereum Smart Contracts
- Flask REST API
- PostgreSQL Database
- JWT Authentication
- Razorpay Payment Integration
- GPS Delivery Verification
- RESTful Architecture
- Cloud Deployment Ready

---

# 🙏 Acknowledgements

Special thanks to:

- Open Source Community
- Flask
- PostgreSQL
- Ethereum
- Web3.py
- Bootstrap
- Razorpay
- GitHub

for providing the tools and technologies that made this project possible.

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the project

🛠️ Contribute improvements

🐛 Report issues

📢 Share with others

---

<div align="center">

# 🌱 Farmers2Market

### Blockchain Enabled Agricultural Marketplace

**Empowering Farmers Through Technology**

Built with ❤️ by **Anoop BP**

⭐ **If you like this project, please give it a Star!**

</div>