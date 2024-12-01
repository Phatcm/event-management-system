## System Design
This document outlines the design decisions, scalability considerations, and data consistency strategies for the RSVP and event management system.

1. Design Decisions
### Technologies
- FastAPI: We use FastAPI as the web framework for this system due to its high performance and ease of use. FastAPI provides asynchronous support, which is ideal for handling multiple concurrent user requests. It also includes automatic API documentation through OpenAPI and supports data validation with Pydantic, reducing boilerplate code and improving development speed.

- SQLAlchemy with AsyncSession: For interacting with the database, we use SQLAlchemy with the asynchronous capabilities of AsyncSession. SQLAlchemy is a well-established ORM for Python, offering robust features for managing database schemas and relationships. The asynchronous support ensures that database operations do not block the server and can handle a large number of concurrent requests, improving overall performance.

- Redis (via redis.asyncio): Redis is used for JWT token blacklisting and caching purposes. This provides fast, in-memory access for checking if a token has been invalidated or expired. Using redis.asyncio allows us to make asynchronous calls to Redis, ensuring non-blocking I/O operations, which improves system performance.

- PostgreSQL: We use PostgreSQL for the relational database due to its strong support for complex queries, data integrity, and scalability. PostgreSQL handles our system's main storage requirements, including users, events, and RSVP data.

- Role-Based Access Control (RBAC): We implement RBAC using a custom middleware (RoleChecker) to ensure that only users with the appropriate roles (e.g., admin, user) can access certain endpoints. This adds a layer of security to the system and ensures that only authorized users can perform specific actions (e.g., creating or managing RSVPs).

### Database Models
- User: A User model stores user-specific details (e.g., user_uid, username, email, and roles). Each user can have multiple RSVPs associated with them, and this relationship is managed by a foreign key to the RSVP model.

- Event: An Event model represents a specific event that users can RSVP to. It includes fields like event_uid, name, date, and capacity. The event’s capacity determines how many users can RSVP for the event.

- RSVP: The RSVP model records each user's participation in an event. It includes the user_uid, event_uid, and status (whether the user is attending, pending, or declined). The model also manages relationships to the User and Event models, ensuring the correct mapping between users and events.

### Trade-offs
- Asynchronous vs Synchronous: We chose asynchronous database operations with SQLAlchemy to handle high concurrent traffic. While synchronous databases may have been simpler to implement, asynchronous support significantly enhances performance and scalability, especially under heavy loads.

- Redis for Blacklisting vs Database: Storing blacklisted JWTs in Redis is a trade-off between simplicity and performance. Redis allows for fast token invalidation without the overhead of querying a database. However, using Redis introduces an additional service to manage, and data persistence could be an issue in case of Redis crashes. This was mitigated by setting an expiration time for JWTs and ensuring they are refreshed regularly.

2. Scalability Considerations
To ensure that the system can handle a large number of users and events, we have considered several approaches:

### Horizontal Scaling
- API Servers: FastAPI’s asynchronous nature makes it easy to scale horizontally by adding more instances behind a load balancer. As the number of requests increases, more FastAPI instances can be deployed to ensure that the system can handle the load. Tools like Kubernetes or Docker Swarm can be used for orchestrating and scaling containers.

- Database Scaling: PostgreSQL supports horizontal scaling through read replicas, which allow us to offload read operations to secondary databases, keeping the primary database focused on write operations. Additionally, sharding or partitioning can be implemented for large datasets (e.g., splitting event and RSVP data across different partitions based on event or user IDs).

- Redis Scaling: Redis can also be horizontally scaled by using Redis clustering. This will allow us to distribute the load across multiple Redis instances, improving performance and reliability when dealing with high traffic.

### Caching
- Event Data Caching: We use Redis for caching frequently requested data, such as event details and user RSVP statuses. This reduces the load on the database, especially for read-heavy operations, and significantly improves response times.

- Session and Token Caching: Redis also plays a critical role in storing session information and invalidating JWT tokens. Storing session data and blacklisted tokens in Redis provides quick access, reducing the need for database queries during every request.

### Auto-scaling and Load Balancing
- Containerization: Kubernetes or similar orchestration services can automatically scale the number of containers running based on system load, ensuring that the system can handle traffic spikes. It can also distribute the load across different containers, ensuring the system remains responsive even with a large number of requests.

Load Balancers: By using a load balancer (such as NGINX or HAProxy), requests can be evenly distributed across available instances, preventing any single instance from becoming a bottleneck.

### Event Capacity Management
- The event model includes a capacity field to track the number of users who have RSVP'd for each event. The system ensures that once the event’s capacity is reached, no further RSVPs can be made. This is enforced at the database level and checked by the RSVP service.

3. Data Consistency
Ensuring data integrity and consistency is critical, especially when managing user RSVPs for events with limited capacity. Below are the approaches used to guarantee consistency:

### Event Capacity Management
- Atomic Operations: When a user RSVPs to an event, the system checks if the event has available capacity. If capacity is available, the RSVP is recorded in the database in an atomic transaction. This prevents race conditions, ensuring that two users cannot simultaneously RSVP for the same spot in an event.

- Optimistic Locking: We use optimistic locking in the RSVP process. If two users attempt to RSVP for the same event simultaneously, the system checks the event’s capacity before allowing the operation. If capacity is reached, the second user is notified that the event is full.

### Database Transactions
- Transactional Integrity: All RSVP-related operations are wrapped in database transactions, ensuring that the system maintains consistent data even in the event of an error. For example, if a user is unable to RSVP to an event due to capacity constraints, the system will roll back the transaction, ensuring that no partial data is saved.

- Event Availability Check: Before processing an RSVP request, the system verifies that the event is still available (i.e., not canceled or closed). This check ensures that users cannot RSVP to events that are no longer active.

### Redis for Token Blacklisting
- Consistency Across Multiple Servers: The Redis store handles token blacklisting in a distributed manner, ensuring that all instances of the API server can check the blacklist for invalid tokens