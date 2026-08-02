\# Farmers2Market - PostgreSQL Database Documentation



\## 1. Database Overview



Farmers2Market uses PostgreSQL as the primary relational database for storing application data.



The database manages:



\* User accounts

\* Farmer profiles

\* Buyer profiles

\* Agricultural products

\* Orders

\* Payments

\* Delivery tracking

\* Blockchain transaction records

\* Audit logs



\## 2. Database Technology



Database:



PostgreSQL



Version:



PostgreSQL 16+



ORM:



SQLAlchemy



Connection:



```

postgresql://username:password@localhost:5432/farmer2market

```



\## 3. Database Architecture



```

&#x20;                   Farmers2Market Backend



&#x20;                           |

&#x20;                           |

&#x20;                      Flask API



&#x20;                           |

&#x20;                           |

&#x20;                     SQLAlchemy ORM



&#x20;                           |

&#x20;                           |



&#x20;                   PostgreSQL Database



&#x20;       -----------------------------------------



&#x20;       Users

&#x20;       Products

&#x20;       Orders

&#x20;       Payments

&#x20;       Delivery

&#x20;       Audit Logs

&#x20;       Blockchain Orders



```



\# 4. Database Configuration



The database configuration is managed using environment variables.



File:



```

.env

```



Example configuration:



```env

DB\_HOST=localhost



DB\_PORT=5432



DB\_NAME=farmer2market



DB\_USER=postgres



DB\_PASSWORD=your\_password





DATABASE\_URL=postgresql://postgres:your\_password@localhost:5432/farmer2market

```



\## 5. Database Tables



\# Users Table



Stores all registered users.



Columns:



| Column        | Type      |

| ------------- | --------- |

| id            | Integer   |

| name          | String    |

| email         | String    |

| password\_hash | String    |

| role          | String    |

| created\_at    | Timestamp |



Roles:



```

farmer

buyer

admin

delivery\_partner

```



\# Products Table



Stores farmer product information.



Columns:



| Column       | Type        |

| ------------ | ----------- |

| id           | Integer     |

| farmer\_id    | Foreign Key |

| product\_name | String      |

| category     | String      |

| quantity     | Float       |

| price        | Float       |

| location     | String      |



\# Orders Table



Stores buyer purchase information.



Columns:



| Column          | Type        |

| --------------- | ----------- |

| id              | Integer     |

| buyer\_id        | Foreign Key |

| product\_id      | Foreign Key |

| quantity        | Integer     |

| total\_amount    | Float       |

| status          | String      |

| blockchain\_hash | String      |



Order Status:



```

Pending



Accepted



Shipped



Delivered



Completed



Cancelled

```



\# Payments Table



Stores transaction details.



Columns:



| Column         | Type        |

| -------------- | ----------- |

| id             | Integer     |

| order\_id       | Foreign Key |

| payment\_method | String      |

| transaction\_id | String      |

| amount         | Float       |

| status         | String      |



\# Delivery Table



Stores delivery tracking details.



Columns:



| Column          | Type        |

| --------------- | ----------- |

| id              | Integer     |

| order\_id        | Foreign Key |

| latitude        | Float       |

| longitude       | Float       |

| delivery\_status | String      |



\# Blockchain Orders Table



Stores blockchain transaction references.



Columns:



| Column            | Type        |

| ----------------- | ----------- |

| id                | Integer     |

| order\_id          | Foreign Key |

| contract\_address  | String      |

| transaction\_hash  | String      |

| blockchain\_status | String      |



\# Audit Logs Table



Maintains system activity records.



Stores:



\* User actions

\* Order updates

\* Payment events

\* Blockchain events



\# 6. Database Relationships



```

User



&#x20;|



&#x20;| 1:N



&#x20;|



Products





User



&#x20;|



&#x20;| 1:N



&#x20;|



Orders





Orders



&#x20;|



&#x20;| 1:1



&#x20;|



Payments





Orders



&#x20;|



&#x20;| 1:1



&#x20;|



Delivery





Orders



&#x20;|



&#x20;| 1:1



&#x20;|



Blockchain Orders



```



\# 7. PostgreSQL Setup



\## Create Database



Open PostgreSQL terminal:



```sql

CREATE DATABASE farmer2market;

```



Connect:



```sql

\\c farmer2market

```



\## Create User



```sql

CREATE USER farmer\_admin WITH PASSWORD 'password';

```



Grant permissions:



```sql

GRANT ALL PRIVILEGES ON DATABASE farmer2market TO farmer\_admin;

```



\# 8. Backend Database Migration



Install dependencies:



```bash

pip install psycopg2-binary

pip install flask-sqlalchemy

```



Run migrations:



```bash

flask db init



flask db migrate



flask db upgrade

```



\# 9. Testing Database Connection



Python test:



```python

from sqlalchemy import create\_engine





DATABASE\_URL = "postgresql://postgres:password@localhost:5432/farmer2market"





engine = create\_engine(DATABASE\_URL)





connection = engine.connect()





print("Database Connected Successfully")





connection.close()

```



\# 10. Backup Database



Create backup:



```bash

pg\_dump farmer2market > backup.sql

```



Restore:



```bash

psql farmer2market < backup.sql

```



\# 11. Production Database Deployment



Recommended production setup:



```

AWS EC2



&#x20;    |



&#x20;    |



Flask Backend



&#x20;    |



&#x20;    |



PostgreSQL Server



&#x20;    |



&#x20;    |



Blockchain Network



```



Security:



\* Strong database password

\* Environment variables

\* Restricted database access

\* Regular backups



\# 12. Database Advantages



\## Reliability



PostgreSQL provides ACID compliant transactions.



\## Scalability



Supports large agricultural marketplace data.



\## Security



Role-based access and encrypted credentials.



\## Integration



Works with Flask, SQLAlchemy, and blockchain services.



\---



\## Farmers2Market Database Summary



PostgreSQL acts as the core data storage layer while Ethereum blockchain provides transparent transaction verification.



The combination ensures:



\* Secure user management

\* Reliable order processing

\* Transparent payments

\* Immutable transaction history



