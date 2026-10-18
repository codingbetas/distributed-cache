from lru_cache import LRUCache

# Create a cache that holds 3 items
cache = LRUCache(capacity=3)

print("Adding A, B, C...")
cache.put("A", "Apple")
cache.put("B", "Banana")
cache.put("C", "Cherry")
print("Cache:", cache)

print("\nAccessing A...")
cache.get("A")
print("Cache:", cache) # A should now be at the front

print("\nAdding D (This should evict B, because it's the least recently used)...")
cache.put("D", "Date")
print("Cache:", cache) 

print("\nAccessing B (Should return None)...")
print(cache.get("B"))