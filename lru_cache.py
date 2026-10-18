class Node:
    """A node in the doubly linked list."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # Hash map: key -> Node
        
        # Dummy head and tail to avoid edge cases during insertion/deletion
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Removes a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node):
        """Adds a node right after the dummy head (Most Recently Used)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str) -> str:
        """Get a value from the cache. If it exists, move it to the front."""
        if key in self.cache:
            node = self.cache[key]
            # Move to front because it was just accessed
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return None

    def put(self, key: str, value: str):
        """Add a value to the cache. If full, evict the LRU item."""
        if key in self.cache:
            # Update existing node and move to front
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            # Create new node
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
            
            # Check if we exceeded capacity
            if len(self.cache) > self.capacity:
                # Evict the Least Recently Used (the one right before the tail)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
                print(f"⚠️ [EVICTED] Key '{lru_node.key}' removed due to capacity limit.")

    def __str__(self):
        """Helper to print the current state of the cache."""
        items = []
        curr = self.head.next
        while curr != self.tail:
            items.append(f"{curr.key}:{curr.value}")
            curr = curr.next
        return " | ".join(items)