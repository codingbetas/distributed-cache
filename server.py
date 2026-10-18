import socket
import threading
from lru_cache import LRUCache

# Define the host and port (using 6379 like real Redis)
HOST = '127.0.0.1'

# Create the cache instance (max 5 items for testing)
cache = LRUCache(capacity=5)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    with conn:
        while True:
            try:
                # Receive data from the client (up to 1024 bytes)
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    break # Client disconnected

                print(f"[{addr}] Received: {data}")
                parts = data.split()
                command = parts[0].upper()

                # Handle Commands
                if command == "SET":
                    if len(parts) < 3:
                        response = "ERROR: Invalid SET syntax. Use 'SET key value'\n"
                    else:
                        key = parts[1]
                        value = " ".join(parts[2:])
                        cache.put(key, value)
                        response = "OK\n"
                        
                elif command == "GET":
                    if len(parts) < 2:
                        response = "ERROR: Invalid GET syntax. Use 'GET key'\n"
                    else:
                        key = parts[1]
                        value = cache.get(key)
                        response = f"{value}\n" if value else "(nil)\n"
                        
                elif command == "DUMP":
                    # A custom command to see the whole cache
                    response = f"Cache: {cache}\n"
                    
                else:
                    response = f"ERROR: Unknown command '{command}'\n"

                # Send the response back to the client
                conn.sendall(response.encode('utf-8'))

            except ConnectionResetError:
                break # Client dropped connection

    print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"🚀 Cache Server is listening on {HOST}:{PORT}...")

    while True:
        # Wait for a connection
        conn, addr = server.accept()
        # Start a new thread to handle this client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    import sys
    # Allow passing a port as an argument, default to 6379
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 6379
    PORT = port
    start_server()