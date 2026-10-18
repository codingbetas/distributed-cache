from consistent_hash import ConsistentHashRing

# Start with 3 cache servers
servers = ["Server-A", "Server-B", "Server-C"]
ring = ConsistentHashRing(nodes=servers)

# Let's see where some keys end up
keys = ["user:1", "user:2", "user:3", "product:99", "session:abc"]
print("--- Distribution with 3 Servers ---")
for key in keys:
    print(f"Key '{key}' -> {ring.get_node(key)}")

# Now, let's simulate adding a 4th server (Scaling out)
print("\n--- Adding Server-D ---")
ring.add_node("Server-D")

# Check where the keys go now
for key in keys:
    print(f"Key '{key}' -> {ring.get_node(key)}")