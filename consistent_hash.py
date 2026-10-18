import hashlib

class ConsistentHashRing:
    def __init__(self, nodes=None, virtual_replicas=3):
        """
        nodes: List of cache server names/IPs
        virtual_replicas: Number of times each node is added to the ring.
                          Higher number = better distribution.
        """
        self.virtual_replicas = virtual_replicas
        self.ring = {}       # Hash value -> Node
        self.sorted_keys = [] # Sorted list of hash values
        self.nodes = set()    # Track unique nodes

        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key: str) -> int:
        """Generate a hash integer (0 to 2^32-1) for a given string."""
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node: str):
        """Adds a new cache server to the ring."""
        self.nodes.add(node)
        for i in range(self.virtual_replicas):
            # Create a unique virtual node name (e.g., "server1-0", "server1-1")
            virtual_node_key = f"{node}-{i}"
            hash_val = self._hash(virtual_node_key)
            self.ring[hash_val] = node
            self.sorted_keys.append(hash_val)
        
        # Keep the keys sorted so we can use binary search later
        self.sorted_keys.sort()

    def remove_node(self, node: str):
        """Removes a cache server from the ring."""
        if node not in self.nodes:
            return
        
        self.nodes.remove(node)
        for i in range(self.virtual_replicas):
            virtual_node_key = f"{node}-{i}"
            hash_val = self._hash(virtual_node_key)
            del self.ring[hash_val]
            self.sorted_keys.remove(hash_val)

    def get_node(self, key: str) -> str:
        """Given a key, find which cache server it belongs to."""
        if not self.ring:
            return None

        hash_val = self._hash(key)
        
        # Find the first node on the ring that is >= the key's hash
        for node_hash in self.sorted_keys:
            if hash_val <= node_hash:
                return self.ring[node_hash]
        
        # If we reached the end of the ring, wrap around to the first node
        return self.ring[self.sorted_keys[0]]
    
    def get_nodes(self, key: str, count: int = 2) -> list:
        """
        Returns a list of 'count' nodes for a given key.
        The first node is the primary, the second is the replica, etc.
        """
        if not self.ring:
            return []
            
        hash_val = self._hash(key)
        nodes = []
        
        # Find the starting point on the ring
        start_idx = 0
        for i, node_hash in enumerate(self.sorted_keys):
            if hash_val <= node_hash:
                start_idx = i
                break
        
        # Walk around the ring to collect unique nodes
        for i in range(len(self.sorted_keys)):
            node_hash = self.sorted_keys[(start_idx + i) % len(self.sorted_keys)]
            node_name = self.ring[node_hash]
            
            if node_name not in nodes:
                nodes.append(node_name)
                if len(nodes) == count:
                    break
                    
        return nodes