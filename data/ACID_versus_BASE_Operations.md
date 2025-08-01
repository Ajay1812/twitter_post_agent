---
datetime: 2025-02-18 16:30
tags:
  - "#ACID"
  - "#BASE"
  - "#usecase"
  - "#Key-Differences"
---
---
## ACID versus BASE consistency models:

![[ACID versus BASE Operations-1739876498369.jpeg]]
## ACID:

*ACID properties ensure reliable transactions in relational databases.*

![[ACID versus BASE Operations-1739877016789.jpeg|400]]

| **Atomicity** – A transaction is all or nothing. If any part fails, the entire transaction is rolled back.                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Consistency** – The database remains in a valid state before and after a transaction.                                                     |
| **Isolation** – Transactions do not interfere with each other, ensuring integrity.                                                          |
| **Durability** – Once a transaction is committed, it remains even in the event of a system crash.                                           |
| Example : ACID is used in traditional **SQL databases** like MySQL, PostgreSQL, and Oracle, ensuring strict data integrity and reliability. |
#### ACID consistency model 
- Used by relational databases 
-  Ensures a performed transaction is always consistent
- Used by: 
	- Financial institutions 
	- Data warehousing
- Databases that can handle many small simultaneous transactions => relational databases
- Fully consistent system

### ACID database use cases:

![[ACID versus BASE Operations-1739876846943.jpeg]]

### NoSQL and BASE models:

- NoSQL has few requirements for immediate consistency, data freshness, and accuracy
- NoSQL benefits: availability, scale, and resilience 
- Used by: 
	- Marketing and customer service companies
	- Social media apps 
	- Worldwide available online services
- Favors availability over consistency of data
- NoSQL databases use BASE consistency model 
- Fully available system

---
## BASE (Basically Available, Soft state, Eventually consistent):

*BASE is a more flexible approach, often used in **NoSQL databases**, prioritizing availability over strict consistency.*

![[ACID versus BASE Operations-1739877204068.jpeg|400]]

| **Basically Available** – Guarantees the database is always available, even if some data is outdated.                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Soft state** – The database state may change over time, even without new transactions.                                                                   |
| **Eventually consistent** – Data will become consistent over time but not immediately after a transaction.                                                 |
| Example : BASE is used in **NoSQL databases** like Cassandra, MongoDB, and DynamoDB, making them suitable for distributed, high-availability applications. |
### BASE database use cases:

![[ACID versus BASE Operations-1739877267767.jpeg]]

---
## Key Differences:

| **Feature**           | **ACID (SQL)**                  | **BASE (NoSQL)**                       |
| --------------------- | ------------------------------- | -------------------------------------- |
| **Consistency Model** | Strict                          | Eventual                               |
| **Scalability**       | Vertical (single server)        | Horizontal (distributed)               |
| **Availability**      | Lower                           | Higher                                 |
| **Use Case**          | Banking, finance, critical apps | Big data, real-time apps, social media |

> [!Summary]
> 
>- **Use ACID** when strong consistency and reliability are required (e.g., banking).
>- **Use BASE** when scalability and availability are priorities (e.g., social media, IoT, big data).



#### References : 

[[Introduction to NoSQL Databases]]