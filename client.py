import socket
from consistent_hash import ConsistentHashRing

# Our 3 cache servers
SERVERS = {
    "Server-A": 6379,
    "Server-B": 6380,
    "Server-C": 6381
}

# Initialize the ring with the server names
ring = ConsistentHashRing(nodes=list(SERVERS.keys()))

def send_to_server(server_name, command):
    """Connects to the specific server and sends a command."""
    port = SERVERS[server_name]
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', port))
        client.sendall((command + "\n").encode('utf-8'))
        response = client.recv(1024).decode('utf-8').strip()
        client.close()
        return response
    except ConnectionRefusedError:
        return f"ERROR: Could not connect to {server_name} on port {port}"

def set_key(key, value):
    # Ask the ring for the top 2 nodes for this key (Replication Factor = 2)
    nodes = ring.get_nodes(key, count=2)
    print(f"📡 Routing SET '{key}' -> Primary: {nodes[0]}, Replica: {nodes[1]}")
    
    # Write to both servers
    response_primary = send_to_server(nodes[0], f"SET {key} {value}")
    response_replica = send_to_server(nodes[1], f"SET {key} {value}")
    
    return response_primary

def get_key(key):
    # Ask the ring for the top 2 nodes
    nodes = ring.get_nodes(key, count=2)
    
    # Try the primary server first
    print(f"📡 Routing GET '{key}' -> Trying Primary: {nodes[0]}")
    response = send_to_server(nodes[0], f"GET {key}")
    
    # If the primary is down or returns (nil), try the replica!
    if "ERROR" in response or response == "(nil)":
        print(f"⚠️ Primary {nodes[0]} failed or missed. Failing over to Replica: {nodes[1]}")
        response = send_to_server(nodes[1], f"GET {key}")
        
    return response

if __name__ == "__main__":
    print("=== Distributed Cache Client ===")
    
    # Let's set some keys
    set_key("user:100", "Himanshu")
    set_key("user:101", "John")
    set_key("product:500", "Laptop")
    set_key("session:xyz", "Active")
    
    print("\n=== Retrieving keys ===")
    print(f"Result: {get_key('user:100')}")
    print(f"Result: {get_key('product:500')}")
    print(f"Result: {get_key('user:999')}") # Should be nil