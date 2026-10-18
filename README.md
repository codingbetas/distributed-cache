# Fault-Tolerant Distributed Cache System

A custom, in-memory distributed cache built entirely from scratch using **raw Python TCP sockets**. No web frameworks (no FastAPI, no Flask). This project demonstrates low-level networking, concurrent programming, and distributed systems concepts.

## 🧠 System Design Concepts Demonstrated

1. **O(1) LRU Eviction Policy:** Uses a Hash Map combined with a Doubly Linked List to achieve O(1) time complexity for `GET` and `PUT` operations. When the cache is full, the Least Recently Used item is evicted.
2. **Raw TCP Sockets:** Implements a custom text-based protocol over TCP, proving an understanding of how network servers actually work under the hood.
3. **Multi-threading & Concurrency:** The server spawns a new thread for every incoming client connection, allowing multiple clients to read/write simultaneously without blocking each other.
4. **Consistent Hashing:** Implements a Consistent Hash Ring to distribute keys across multiple cache nodes. Adding or removing a node only remaps a fraction of the keys, preventing massive cache misses.
5. **High Availability (Replication):** Implements a Replication Factor (RF=2). When a key is written, it is saved to both a **Primary** and a **Replica** node. If the Primary node goes down, the client automatically fails over to the Replica, ensuring zero downtime.

## 🏗️ Architecture

```text
       ┌──────────────┐
       │    Client    │
       └──────┬───────┘
              │
       ┌──────▼───────┐
       │ Consistent   │  <-- Hashes the key to find Primary & Replica
       │ Hash Ring    │
       └──────┬───────┘
              │
      ┌───────┼───────┐
      ▼       ▼       ▼
 ┌────────┐┌────────┐┌────────┐
 │Server A││Server B││Server C│
 │ (TCP)  ││ (TCP)  ││ (TCP)  │
 └────┬───┘└────┬───┘└────┬───┘
      │         │         │
      ▼         ▼         ▼
 ┌────────┐┌────────┐┌────────┐
 │ LRU    ││ LRU    ││ LRU    │
 │ Cache  ││ Cache  ││ Cache  │
 └────────┘└────────┘└────────┘
```

## 📂 Project Structure

- `lru_cache.py` — The core data structure (Hash Map + Doubly Linked List).
- `server.py` — The TCP server that listens for commands and handles concurrent clients via threads.
- `consistent_hash.py` — The Consistent Hash Ring implementation.
- `client.py` — The client that hashes keys, writes to Primary/Replica, and handles failover.
- `test_lru.py` — Unit test for the LRU eviction logic.
- `test_hashing.py` — Script to demonstrate how keys map to the hash ring.

## 🚀 How to Run

**1. Start 3 Cache Servers (in 3 separate terminals):**

```bash
# Terminal 1
python server.py 6379

# Terminal 2
python server.py 6380

# Terminal 3
python server.py 6381
```

**2. Run the Distributed Client:**

```bash
python client.py
```

You will see the client hash the keys, route them to different servers, and retrieve the correct data.

## 🛡️ Testing Fault Tolerance (Failover)

To prove the system is fault-tolerant:
1. While the servers are running, run `python client.py` to seed the data.
2. Go to one of the server terminals (e.g., Server-C on port 6381) and press `Ctrl + C` to kill it.
3. Run `python client.py` again.

The client will detect that the Primary node is down, automatically failover to the Replica node, and successfully retrieve the data.

## 📄 License

MIT